import sys

# NOTE : whe topic ids are not integers pls change in preranked as well as data
filepath = sys.argv[1]
filepath_out = sys.argv[2]

preranked_file = sys.argv[3]
# map of topics, each will be a map of doc ids
preranked = {} # {topic} => {doc id} -> score  score is 0,1 if qrel

with open(preranked_file, 'r') as inputFile:
    for line in inputFile:
        #parts = line.split("\t")
        parts = line.split()
        #topicId = int(parts[0].strip())
        topicId = parts[0].strip()
        if topicId not in preranked:
            preranked[topicId] = {}
        
        docid = parts[1].strip()
        
        preranked[topicId][docid] = parts[2].strip()
        # preranked.append((int(parts[0].strip()), parts[1].strip(), parts[2].strip()))
        #preranked.append((parts[0].strip(), parts[1].strip(), parts[2].strip()))

data = {}

with open(filepath ,'r') as inputFile:
    for line in inputFile:
        parts = line.split()
        #parts = line.split("\t")
    
        #topicId = int(parts[0].strip())
        topicId = parts[0].strip()
        docId = parts[1].strip()
        score = float(parts[2].strip())

        if topicId not in data:
            data[topicId] = []

        data[topicId].append((score, docId))

#print(data)
#print(preranked)
for topic in sorted(data):
    list = data[topic]
    for i in range(len(list)):
        score, docId = list[i]
        
        if topic in preranked and docId in preranked[topic]:
            preranked_score = preranked[topic][docId]
            list[i] = (score * float(preranked_score), docId)

with open(filepath_out ,'w') as outFile:
    for topic in sorted(data):
        i = 0
        for tuple in sorted(data[topic],reverse=True):
            if i == 1000:
                break
            outFile.write(str(topic)+'\t0\t'+tuple[1]+'\t'+str(i)+'\t'+str(tuple[0])+'\tdrmm\n')
            i += 1
            
