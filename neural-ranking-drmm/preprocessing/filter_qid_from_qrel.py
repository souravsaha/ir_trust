# input : <unique qrel file>, <preranked file> <output filtered file>
# idea is to take unique ids from the preranked file and filter those ids from qrel file

import os
import sys

qrel_file = sys.argv[1]
preranked_file = sys.argv[2]
output_filtered_qrel_file = sys.argv[3]

prerank_qids = []
with open(preranked_file, 'r') as input_preranked_file:
    for line in input_preranked_file:
        prerank_qids.append(line.split("\t")[0].strip())

prerank_qids_set = set(prerank_qids)
print(prerank_qids_set)

with open(output_filtered_qrel_file, 'w') as outputFile:
    with open(qrel_file, 'r') as input_qrel:
        for line in input_qrel:
            qid = line.split("\t")[0].strip()
            if qid in prerank_qids_set:
                outputFile.write(line)

    
