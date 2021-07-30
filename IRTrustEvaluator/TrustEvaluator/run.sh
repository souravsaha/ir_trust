#!/bin/bash
mvn compile


INDEX=/user1/faculty/cvpr/irlab/collections/indexed/index_lucene_5.3
#QUERY=/user1/faculty/cvpr/irlab/sourav/ir_trust/msmarco-test2019-queries.tsv
#QUERY=/user1/faculty/cvpr/irlab/sourav/ir_trust/IRTrustEvaluator/TrustEvaluator/topics.xml
QUERY=/user1/faculty/cvpr/irlab/sourav/ir_trust/robust-uqv.txt
FEEDBACK=true
#QRELS=/user1/faculty/cvpr/irlab/sourav/ir_trust/2019qrels-pass_train.txt
QRELS=/user1/faculty/cvpr/irlab/sourav/ir_trust/IRTrustEvaluator/TrustEvaluator/qrels.trec678.adhoc
RESFILE=/user1/faculty/cvpr/irlab/sourav/ir_trust/res_files/trec_uqv_res/kderlm/lm/

#for k in 2 5 8 10 20 30 50
#do
#for b in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 
#do
#for k in 0.8 0.9 1.0 1.1 1.2
#do
#for b in 0.5 0.6 0.7 0.8 0.9 1.0

#for k in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9
#do

for h in 1 2 5 10
do 
for sigma in 10 20 50 
do 
cat > retrieve.properties << EOF1
index=$INDEX

#result file path
#res.file=$RESFILE+$k+$b
res.file=$RESFILE+$h+$sigma

#query file path
query.file=$QUERY


#feedback used or not
feedback=$FEEDBACK

#evaluation flag
eval=false

#number of topdocs used for feedback
fdbk.numtopdocs=10

#stopwordFile
stopfile=stop.txt

qrels.file=$QRELS

#number of topdocs retrieved
retrieve.num_wanted=1000
#evaluate.graded=true

#query expansion using rlm flag
rlm.qe=true

#query expansion term weight using rlm
rlm.qe.newterms.wt=0.3

#number of expansion terms
rlm.qe.nterms=10

#collection Trec/MSMARCO
collection=Trec

#evaluation mode
evalMode=trust1

#rlm type (uni, bi, iid, conditional)
rlm.type=rlm_conditional

#kde sigma value
gaussian.sigma=$sigma

#kde h value
kde.h=$h

#kde kernel type
kde.kernel=gaussian

#wordvec file
#wordvecs.vecfile=C:/Users/Procheta/Downloads/tmp.vec
wordvecs.vecfile=/user1/faculty/cvpr/irlab/collections/w2v-trained/external/wiki2013-analyzed.vec

#wordvec file type
wordvecs.readfrom=vec

#retrieval model (BM25,LM)
retrieveModel=LM

#querypairs file path
#querypairs.file=C:/Users/Procheta/Downloads/robust-uqv.txt

querypairs.file=/user1/faculty/cvpr/irlab/sourav/ir_trust/robust-uqv.txt


fieldName=words
k=0.8
b=0.5
lambda=0.7 

EOF1
#echo "k $k"
#echo "b $b"
mvn exec:java@retrieve -Dexec

done
done
