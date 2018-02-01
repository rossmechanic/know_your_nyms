import json

jsonList = []

count = 1
index = 0
f = open('concreteness_scores.txt', 'r')
for line in f:
	jsonFile = {}
	# avg_score, total_rounds, total_score
	l = line.rstrip().split('\t')
	jsonFile["model"]="NLP4CCB.ConcretenessStat"
	jsonFile["pk"]=count
	fields={}
	fields["word"] = l[0]
	fields["index"] = index
	fields["sem_rel"] = "concreteness"
	fields["avg_score"] = float(l[1])
	fields["total_score"] = float(l[3])
	fields["rounds_played"] = int(l[2])
	jsonFile["fields"] = fields
	count += 1
	index += 1
	jsonList.append(jsonFile)
with open('data.json', 'w') as outfile:
    json.dump(jsonList, outfile)
f.close()