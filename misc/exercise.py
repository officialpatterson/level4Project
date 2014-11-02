#13/10/2014
#the script below takes in a json file of twitter objects and a file of the manual evaluation results.
# the output of the script is a collection of tuples that contain the tweet text and the reputation.
import json, csv, nltk


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
    tokens = tokens = nltk.word_tokenize(tweet)
    trainingSet.append((tokens, dimension))


word_features = get_word_features(get_words_in_tweets(trainingSet[0:1024]))
training_set = nltk.classify.apply_features(extract_features, trainingSet)
classifier = nltk.NaiveBayesClassifier.train(training_set)


#Attempt testing. print the collection size along with the number of tweets defined by each reputation. 
collection = buildTrainingSet(loadTweets())
correctLabels = 0
incorrectLabels = 0
sampleSize = 1024
n= 1024
#loop for all the tweets and attempt classification
for i in range(n,n+sampleSize):
	tweet_text = collection[i][0]
	tweet_dimension = collection[i][1]
	classification = classifier.classify(extract_features(tweet_text.split()))
	print '--------------Test ',i,'--------------'
	print '\tExpected Result: ', tweet_dimension
	print '\tActual Result: ', classification
	if classification == tweet_dimension:
		correctLabels += 1
	else:
		incorrectLabels += 1
print '\n\n\n\n\n\n\n--------------Test Summary--------------'
print 'Collection Size: ', sampleSize
print 'Correct labelling: ', correctLabels
print 'Incorrect labelling: ', incorrectLabels
print 'accuracy: ', nltk.classify.accuracy(classifier, collection[n:sampleSize])
print(nltk.classify.accuracy(classifier, collection[n:sampleSize]))
classifier.show_most_informative_features()


