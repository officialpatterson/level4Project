#13/10/2014
#the script below takes in a json file of twitter objects and a file of the manual evaluation results.
# the output of the script is a collection of tuples that contain the tweet text and the reputation.
import sys, os, nltk
from Twitter4AP import TwitterRest
from pymongo import errors
from pymongo import MongoClient
import json,time, csv
from time import gmtime, strftime


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
	
	for tweet in tweets:
		collection.append((tweet['text'].encode('utf8'), goldStandardSet[tweet['id']]))
	return collection

def get_words_in_tweets(tweets):
    all_words = []
    for (words, dimension) in tweets:
      all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

###########################	MAIN ROUTINE		     ##########################

#Build Classifier and train
trainingSet = []
for (tweet,dimension) in buildTrainingSet(loadTweets()):
    tokens = [e.lower() for e in tweet.split() if len(e) >= 3]
    trainingSet.append((tokens, dimension))


word_features = get_word_features(get_words_in_tweets(trainingSet))
training_set = nltk.classify.apply_features(extract_features, trainingSet)
classifier = nltk.NaiveBayesClassifier.train(training_set)

####################### LIVE CLASSIFICATION ##########################
#setup entitylist
client = MongoClient()
db = client.GTBT
s = TwitterRest()
entityList = []

with open("entities.tsv") as tsv:
    for line in csv.reader(tsv, dialect="excel-tab"):
        entityList.append(line[0])

#search for the entity on twitter and for each tweet recieved classify
print 'Classifying...'
while True:
    for e in entityList:
        result = s.search({'q':e, 'lang':'en'})
        statuses = json.loads(result.text)
        for status in statuses['statuses']:
            status['entity'] = e #append the entity name to the tweet
            tweet_text = status['text']
            status['class'] = classification = classifier.classify(extract_features(tweet_text.split()))
            collection = db.classifications
            collection.insert(status)
            
    time.sleep(180)


