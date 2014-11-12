#13/10/2014
#Purpose: Create a (naive)bayesian probability model based on boolean features of an entity.
#No stemming, tokenized only on spaces.
#only uses the x most common words in the collection as possibile features
import nltk, json, csv, random
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from Tweet import Tweet
###########################	 LOADING DATA #########################

def loadTweets():
    tweets = []
    goldStandardSet = {}
    collection = []
    with open('preliminary_data/pre.3ent.json')  as f:
        for line in f:
	    tweets.append(Tweet(json.loads(line)))

	#load gold standard
	with open("preliminary_data/pre.3ent.tsv") as tsv:
   		for line in csv.reader(tsv, dialect="excel-tab"):
			goldStandardSet[int((line[1]))] = line[2]
	
	for tweet in tweets:
		tweet.set_label(goldStandardSet[tweet.id])
    return tweets

###########################	 SUBROUTINES #########################
def tweet_features(tweet, all_words):
    tweet_words = set(tweet.text)
    features = {}
    
    for word in all_words:
        features['contains %s' % word] = (word in tweet_words)
    return features

def cleanTweet(tweet):
    stemmer = nltk.stem.porter.PorterStemmer()
    tokensArray = []
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(tweet.text)
    for token in tokens:
        token = stemmer.stem(token)
        if token not in stopwords.words('english'):
		if(len(token) < 2):
			continue
        	tokensArray.append(token)
    tweet.text = tokensArray

def generateVocabulary(tweets):
    vocab = []
    for token in tweet.text:
	vocab.append(token)
    freqDist = nltk.FreqDist(vocab)
    return freqDist
####################### Main Routine ##########################
tweets = loadTweets()
random.shuffle(tweets)
tweets = [cleanTweet(tweet) for tweet in tweets]
all_words = generateVocabulary(tweets).keys()
featureSet = [(tweet_features(tweet, all_words),tweet.label) for tweet in tweets]

limit = 1700
training_set = featureSet[:limit]
test_set = featureSet[limit:]

classifier = nltk.NaiveBayesClassifier.train(training_set)
####################### CLASSIFIER ANALYSIS ##########################
print 'Vocab Size: ',len(all_words)
print 'size of collection: ', len(tweets)
print 'accuracy: ',nltk.classify.accuracy(classifier, test_set)
print classifier.show_most_informative_features()
####################### LIVE CLASSIFICATION ##########################


