#13/10/2014
#the script below takes in a json file of twitter objects and a file of the manual evaluation results.
# the output of the script is a collection of tuples that contain the tweet text and the reputation.
from Twitter4AP import TwitterRest
from pymongo import errors, MongoClient
import json, csv, nltk, time
from classifiers.naivebayes import *

#setup entitylist
client = MongoClient()
db = client.GTBT
s = TwitterRest()
entityList = []

with open("entities.tsv") as tsv:
    for line in csv.reader(tsv, dialect="excel-tab"):
        entityList.append(line[0])

####################SETUP CLASSIFIER##############################
print 'Training Classifier...'
tweets = loadTweets()
random.shuffle(tweets)
tweets = [(cleanTweet(tweet), label) for (tweet, label) in tweets]
all_words = generateVocabulary(tweets).keys()
featureSet = [(tweet_features(tweet, all_words), label) for (tweet, label) in tweets]

size = len(featureSet)
training_set = featureSet[:size/2]
test_set = featureSet[size/2:]


classifier = nltk.NaiveBayesClassifier.train(training_set)
acc = nltk.classify.accuracy(classifier, test_set)
print acc
print '...Classifier trained. Classifier ready for use acc: %d ' % acc

#search for the entity on twitter and for each tweet recieved classify
print 'Classifying...'
while True:
    for e in entityList:
        result = s.search({'q':e, 'lang':'en'})
        statuses = json.loads(result.text)
        for status in statuses['statuses']:
            status['entity'] = e #append the entity name to the tweet
            tweet_text = status['text']
            label = classifier.classify(tweet_features(tweet_text, all_words))
            status['class'] = label
            collection = db.classifications
            collection.insert(status)
    time.sleep(180)


