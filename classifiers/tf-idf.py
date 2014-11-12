import csv, json
def loadTweets():
    tweets = []
    goldStandardSet = {}
    collection = []
    labelCount = {}
    with open('preliminary_data/pre.3ent.json')  as f:
        for line in f:
            tweets.append(json.loads(line))

	#load gold standard
	with open("preliminary_data/pre.3ent.tsv") as tsv:
   		for line in csv.reader(tsv, dialect="excel-tab"):
			goldStandardSet[int((line[1]))] = line[2]
	
	for tweet in tweets:
		collection.append((tweet['text'], goldStandardSet[tweet['id']]))
    return collection

tweets = loadTweets()
print len(tweets)

with open('tweets.json','w') as f:
	f.write(json.dumps(tweets))
