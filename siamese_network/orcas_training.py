# import the library
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from collections import defaultdict
import random as r
import math as m
import numpy as np
from keras import backend as K
from random import Random
from nltk.tokenize import word_tokenize
import pandas as pd
import sys
import nltk
import keras.preprocessing.text
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from keras.preprocessing import sequence
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Flatten, Embedding, LSTM, Bidirectional, Concatenate
from keras.layers import Input, Lambda
from keras.optimizers import Adam
from keras.optimizers import RMSprop


BASEDIR = 'core/prediction/'
TRAIN_FILE = BASEDIR + 'sentences/train.tsv'
PT_VEC_FILE = BASEDIR + 'graphs/nodevecs/nodes_and_words.vec'
INTERVENTION_SIM_THRESHOLD = 0.1

MAXLEN = 50
SEED=314159 # first digits of Pi... an elegant seed!
MODEL_FILE= 'trust_query_pairs.h5'


df = pd.read_csv(sys.argv[1])

# create vocabulary
nltk.download('punkt')
# df = pd.read_csv('trust_query_pairs.csv')
corpora = []
# remove the double quotation from the string
df['query'] = df['query'].str.replace('"', '')
df['variant'] = df['variant'].str.replace('"', '')

corpora = df['query'].tolist()
corpora += df['variant'].tolist()

#print(corpora) 

word_tokenizer = Tokenizer()
word_tokenizer.fit_on_texts(corpora)
vocab_length = len(word_tokenizer.word_index) + 1

print(vocab_length)
embedded_sentences = word_tokenizer.texts_to_sequences(corpora)
#print(embedded_sentences)

#voc = word_tokenizer.ge
#word_index = dict(zip(voc, range(len(voc))))'
print(word_tokenizer)


word_count = lambda sentence: len(word_tokenize(sentence))
longest_sentence = max(corpora, key=word_count)
max_len = len(word_tokenize(longest_sentence))

print('longest sentencs: ', longest_sentence)
#print(corpora)
print(max_len)

df_query_1 = df["query"].to_numpy() 
df_query_2 = df["variant"].to_numpy()

query_1 = word_tokenizer.texts_to_sequences(df_query_1)
query_2 = word_tokenizer.texts_to_sequences(df_query_2)

query_1 = pad_sequences(query_1, max_len, padding='post')
query_2 = pad_sequences(query_2, max_len, padding='post')

x_train = np.hstack([query_1, query_2])
#x_train = np.vstack([df_query_1, df_query_2])
#x_train = np.transpose(x_train)
y_train = df["clicked"].to_numpy()

print("y_train before: ", y_train)

y_train = np.where(y_train < 1 , y_train, 1)  # be careful here

print("y_train : ", y_train)
#np.savetxt("foo.csv", y_train, delimiter=",")

# I think there is some problem
row, _ = x_train.shape
#np.savetxt("foo.csv", x_train, delimiter=",")
'''
for i in range(row):
    #col = x_train[i].shape
    col = np.shape(a)[i]
    if col != 200:
        print("Column is not 200", col)
    #print(col)
print("x_train shape: ",x_train[0].shape)
'''
print(x_train.shape)

print(df_query_1[0])

import os
#path_to_glove_file = os.path.join(
#    os.path.expanduser("~"), ".keras/datasets/glove.6B.300d.txt"
#)
path_to_glove_file ='/user1/faculty/cvpr/irlab/collections/w2v-trained/external/wiki2013/wiki2013-analyzed.vec'
embeddings_index = {}
with open(path_to_glove_file) as f:
    for line in f:
        word, coefs = line.split(maxsplit=1)
        coefs = np.fromstring(coefs, "f", sep=" ")
        embeddings_index[word] = coefs

print("Found %s word vectors." % len(embeddings_index))

num_tokens = vocab_length + 2
embedding_dim = 200
hits = 0
misses = 0

# Prepare embedding matrix
embedding_matrix = np.zeros((num_tokens, embedding_dim))
for word, i in word_tokenizer.word_index.items():
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        # Words not found in embedding index will be all-zeros.
        # This includes the representation for "padding" and "OOV"
        #print(word)
        #print(embedding_vector)
        embedding_matrix[i] = embedding_vector
        hits += 1
    else:
        misses += 1
print("Converted %d words (%d misses)" % (hits, misses))

print(embedding_matrix.shape[0])
print(embedding_matrix.shape[1])
print(embedding_matrix)


LSTM_DIM = 32
#LSTM_DIM = 48
DROPOUT = 0.2

from keras.layers.merge import concatenate

def complete_model():
    
    input_a = Input(shape=(max_len, ))    
    print (input_a.shape)
    
    emb_a = Embedding(embedding_matrix.shape[0],
                  embedding_matrix.shape[1],
                  weights=[embedding_matrix])(input_a)
    print (emb_a.shape)
    
    input_b = Input(shape=(max_len, ))    
    print (input_b.shape)
    
    emb_b = Embedding(input_dim=embedding_matrix.shape[0],
                  output_dim=embedding_matrix.shape[1],
                  weights=[embedding_matrix])(input_b)
    print (emb_b.shape)
    
    shared_lstm = LSTM(LSTM_DIM)

    # because we re-use the same instance `base_network`,
    # the weights of the network
    # will be shared across the two branches
    processed_a = shared_lstm(emb_a)
    processed_a = Dropout(DROPOUT)(processed_a)
    processed_b = shared_lstm(emb_b)
    processed_b = Dropout(DROPOUT)(processed_b)

    merged_vector = concatenate([processed_a, processed_b], axis=-1)
    # And add a logistic regression (2 class - sigmoid) on top
    # used for backpropagating from the (pred, true) labels
    predictions = Dense(1, activation='sigmoid')(merged_vector)
    
    model = Model([input_a, input_b], outputs=predictions)
    return model    

def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

def buildModel():
    model = complete_model()
    '''
    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    '''
    # add precision, recall to the metric
    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy',
                  metrics=['accuracy', f1_m, precision_m, recall_m])
    return model

def trainModel(model, x_train, x_test, y_train, y_test):
    #EPOCHS = 1
    EPOCHS = 20
    #BATCH_SIZE = 1000
    BATCH_SIZE = 128
    history = model.fit([x_train[:, max_len], x_train[:, max_len: 2*max_len]], y_train,
              batch_size=BATCH_SIZE,
              epochs=EPOCHS,
              # validation_data=([x_val[:, max_len], x_val[:, max_len: 2*max_len]], y_val),
              validation_data=([x_test[:, max_len], x_test[:, max_len: 2*max_len]], y_test),
              verbose=True
             )

    model.save_weights(MODEL_FILE)
    return history

from sklearn.model_selection import KFold
from matplotlib import pyplot as plt
kf = KFold(n_splits = 5, random_state=None, shuffle=True) # TODO : make shuffle = True 

total_accuracy = 0
total_f1_score = 0
total_precision = 0
total_recall = 0

for train_index, test_index in kf.split(x_train):
  model = buildModel()
  model.summary()
  # print("TRAIN:", train_index, "TEST:", test_index)
  X_train, X_test = x_train[train_index], x_train[test_index]
  Y_train, Y_test = y_train[train_index], y_train[test_index]
  
  print(X_train.shape)
  print(X_test.shape)
  print(Y_train.shape)
  print(Y_test.shape)

  history = trainModel(model, X_train, X_test, Y_train, Y_test)
  # plot the curve
  plt.plot(history.history['accuracy'])
  plt.plot(history.history['val_accuracy'])
  plt.title('model accuracy')
  plt.ylabel('accuracy')
  plt.xlabel('epoch')
  plt.legend(['train', 'val'], loc='upper left')
  plt.show()
  loss, accuracy, f1_score, precision, recall = model.evaluate([X_test[:, max_len], X_test[:, max_len: 2*max_len]], Y_test, verbose=0)
  y_pred = model.predict([X_test[:, max_len], X_test[:, max_len: 2*max_len]])
  # print('y_pred: ', y_pred.shape)
  # print('loss: ', loss)
  # print('accuracy: ', accuracy)
  # print('f1:', f1_score)
  # print('precision: ', precision)
  # print('recall: ', recall)
  total_accuracy += accuracy
  total_recall += recall
  total_f1_score += f1_score
  total_precision += precision
  
  # model.load_weights(MODEL_FILE) # TODO : remove ... redundant 
  K.clear_session()
  del model 

print('Avg accuracy: ', total_accuracy /5)
print('Avg recall: ', total_recall /5)
print('Avg f1 score: ', total_f1_score /5)
print('Avg precision: ', total_precision /5)
