# ir_trust
## Setup
To generate the fairness score use the following:
```
Run model_fairness_score.py (inside code repo), you need to pass 4 arguments to the program. 
Argument 1 : result file
Argument 2 : query file (TrecRb)
Argument 3 : top k documents (k = 5, 10 etc.)
Argument 4 : fairness metric type (j - jaccard, wj - weighted jaccard) 

Example run:
python3 model_fairness_score.py ../res_files/lmdir-100 ../robust-uqv.txt 5 wj

```
