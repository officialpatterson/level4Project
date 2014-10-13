#13/10/2014
#the script below takes in a json file of twitter objects and a file of the manual evaluation results.
# the output of the script is a collection of tuples that contain the tweet text and the reputation.
import json, csv


###########################	 SUBROUTINE DEFINITIONS BELOW #########################
def loadTweets():
	tweets = []
	with open('preliminary_data/pre.3ent.json')  as f:
    		for line in f:
        		tweets.append(json.loads(line))

	return tweets

def buildTrainingSet(tweets):
	goldStandardSet = {}
	collection = []
	#load gold standard
	with open("preliminary_data/pre.3ent.tsv") as tsv:
   		for line in csv.reader(tsv, dialect="excel-tab"):
			goldStandardSet[int((line[1]))] = line[2]
	

	print 'BUILDING COLLECTION...'	
	for tweet in tweets:
		collection.append((tweet['text'].encode('utf8'), goldStandardSet[tweet['id']]))
	print '...COMPLETE'
	
	return collection

###########################	MAIN ROUTINE		     ##########################
collection = buildTrainingSet(loadTweets())
