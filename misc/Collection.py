import json, csv

def buildSet():
	tweets = []
	with open('preliminary_data/pre.3ent.json')  as f:
    		for line in f:
        		tweets.append(json.loads(line))
	

	goldStandardSet = {}
	collection = []
	#load gold standard
	with open("preliminary_data/pre.3ent.tsv") as tsv:
   		for line in csv.reader(tsv, dialect="excel-tab"):
			goldStandardSet[int((line[1]))] = line[2]
	
	for tweet in tweets:
		collection.append((tweet['text'].encode('utf8'), goldStandardSet[tweet['id']]))
	return collection

t = buildSet()
print t
