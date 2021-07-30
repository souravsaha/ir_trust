#!/bin/bash
#k = $1
#b = $2
cat > retrieve.properties << EOF1

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

#result file path
res.file=/user1/faculty/cvpr/irlab/sourav/ir_trust/res_files/trec
#query file path
query.file=/user1/faculty/cvpr/irlab/sourav/ir_trust/IRTrustEvaluator/TrustEvaluator/topics.xml

#index path
index=/user1/faculty/cvpr/irlab/collections/indexed/index_lucene_5.3/

#feedback used or not
feedback=false

#evaluation flag
eval=true

#number of topdocs used for feedback
fdbk.numtopdocs=5

#stopwordFile
stopfile=/user1/faculty/cvpr/irlab/sourav/ir_trust/IRTrustEvaluator/TrustEvaluator/stop.txt
qrels.file=/user1/faculty/cvpr/irlab/sourav/ir_trust/IRTrustEvaluator/TrustEvaluator/qrels.trec678.adhoc

#stopfile=C:/Users/Procheta/Documents/Indexes/kderlm-master/stop.txt
#qrels.file=C:/Users/Procheta/Downloads/TrustEvaluator/data/qrels/qrels.trec6.adhoc
#number of topdocs retrieved
retrieve.num_wanted=1000
#evaluate.graded=true

#query expansion using rlm flag
rlm.qe=false

#query expansion term weight using rlm
rlm.qe.newterms.wt=0.7

#number of expansion terms
rlm.qe.nterms=10

#collection Trec/MSMARCO
collection=TrecAdhoc

#evaluation mode
evalMode=trust1

#rlm type (uni, bi, iid, conditional)
rlm.type=bi

#kde sigma value
gaussian.sigma=10

#kde h value
kde.h=1

#kde kernel type
kde.kernel=gaussian

kde.compose=true

#wordvec file
wordvecs.vecfile=/user1/faculty/cvpr/irlab/collections/glove/glove.840B.300d.vec
#wordvecs.vecfile=C:/Users/Procheta/Downloads/tmp.vec

#wordvec file type
wordvecs.readfrom=vec

#retrieval model (BM25,LM)
retrieveModel=LM
#k = $1
#b = $2
lambda = $1

#querypairs file path
querypairs.file=/user1/faculty/cvpr/irlab/sourav/ir_trust/robust-uqv.txt

fieldName=words

EOF1

sh run.sh
