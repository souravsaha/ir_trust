'''
argument 1: result file
argument 2: query file
argument 3: top k document (value of k) k = 5, 10
argument 4: metric type "j" - jaccard, "wj" - weighted jaccard
'''

import sys
import itertools
import math

#qid_doc_list_map = {}

# parse the result file. Extracts qid and docid
def process_res_file(resfile):
    
    qid_doc_list_map = {}
    resfile_content = open(resfile, 'r')
    for line in resfile_content:
        split_line = line.split("\t")
        qid = split_line[0]
        docid = split_line[2]
        if qid not in qid_doc_list_map:
            doc_ids = []
            doc_ids.append(docid)
            qid_doc_list_map[qid] = doc_ids
        else:
            old_list = qid_doc_list_map[qid]
            old_list.append(docid)
            qid_doc_list_map[qid] = old_list
    
    resfile_content.close()
    return qid_doc_list_map


def process_query_file(queryfile):
    qid_user_session_map = {}
    
    queryfile_content = open(queryfile, 'r')
    for line in queryfile_content:
        qid = line.split(";")[0]
        #print(qid)
        qid_split =  qid.split("-")
        
        qid_sess = qid_split[0] + "-" + qid_split[1]
        
        if qid_sess not in qid_user_session_map:
            query_ids = []
            query_ids.append(qid)
            qid_user_session_map[qid_sess] = query_ids
        else:
            old_list = qid_user_session_map[qid_sess]
            old_list.append(qid)
            qid_user_session_map[qid_sess] = old_list
            
        #print(qid)

    return qid_user_session_map


#define Jaccard Similarity function
def jaccard(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union

# weighted jacard: Earlier version: where we considered only intersection of two lists
'''
def weighted_jaccard(list1, list2):
    intersection_list = (list(set(list1).intersection(list2)))
    weighted_jaccard_score = 0

    for item in intersection_list:
        list1_rank = list1.index(item)
        list2_rank = list2.index(item)
        x = (list1_rank - list2_rank)**2
        weighted_jaccard_score += math.exp(-x)

    return weighted_jaccard_score
'''
def union(list1, list2):
    final_list = list(set(list1) | set(list2))
    return final_list

# weighted jaccard , define max list rank = 1000
def weighted_jaccard(list1, list2):
    union_list = union(list1, list2)
    weighted_jaccard_score = 0.0
    for docid in union_list:
        list1_rank = 100        # default values
        list2_rank = 100        # default values
        if docid in list1: 
            list1_rank = list1.index(docid)
        if docid in list2:
            list2_rank = list2.index(docid)
        
        x = (list1_rank - list2_rank)**2
        weighted_jaccard_score += math.exp(-x)
    
    normalized_score = weighted_jaccard_score / len(union_list)
    return normalized_score


resfile = sys.argv[1]     # res file path as an argument
queryfile = sys.argv[2]   # query file path as an argument
k = sys.argv[3]           # parameter for top k
k = int(k)
metric = sys.argv[4]      # on which metric you want to evaluate j- inverse-jacard, wj- weighted inverse jacard

qid_doc_list_map = process_res_file(resfile)
qid_user_session_map = process_query_file(queryfile)

total_fairness_score = 0.0
qid_user_count  = 0 

print("All pairs")
for qid_user in qid_user_session_map:
    qid_user_pairs = qid_user_session_map[qid_user]
    if len(qid_user_pairs) > 1:
        #print(qid_user_pairs)
        qid_user_count += 1

        pair_count = 0 
        model_fairness_score = 0.0
        for pair in itertools.combinations(qid_user_pairs , 2):
            print(pair[0], pair[1])
            #print(qid_doc_list_map[pair[0]])#print(qid_doc_list_map[pair[1]])
            # truncate to top k 
            if pair[0] in qid_doc_list_map and pair[1] in qid_doc_list_map:

                docids_pair_1 = qid_doc_list_map[pair[0]]
                docids_pair_2 = qid_doc_list_map[pair[1]]
            
                del docids_pair_1[k:]
                del docids_pair_2[k:]
            
                #print(docids_pair_1)
                #print(docids_pair_2)
                
                if metric == "j":
                    inverse_jacard = 1 - jaccard(docids_pair_1, docids_pair_2)
                    model_fairness_score += inverse_jacard
                if metric == "wj":
                    inverse_weighted_jacard = 1 - weighted_jaccard(docids_pair_1, docids_pair_2)
                    model_fairness_score += inverse_weighted_jacard
                    #print(model_fairness_score)

                pair_count += 1
        
        if pair_count > 0 :
            total_fairness_score += (model_fairness_score / pair_count)
            
            #print(total_fairness_score)
                #print(len(qid_doc_list_map[pair[0]]))
                #print(len(qid_doc_list_map[pair[1]]))
                #compu fetch the list of the pair; truncate to top k ; and just compute
            
#print(model_fairness_score)
print("Trust Metric score ", total_fairness_score/qid_user_count)
#print(qid_doc_list_map)
#print(qid_user_session_map)

