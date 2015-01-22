#13/10/2014
#the script below takes in a json file of twitter objects and a file of the manual evaluation results.
# the output of the script is a collection of tuples that contain the tweet text and the reputation.
from Twitter4AP import TwitterRest
from pymongo import errors, MongoClient
import json, csv, nltk, time
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

def loadTweets():
    
    tweets = []
    goldStandardSet = {}
    collection = []
    
    client = MongoClient()
    db = client.gtbt
    
    for doc in db.classifications.find({"gold":"True"}):
        collection.append((doc['tweet'],doc['dimension']))

    

    with open('preliminary_data/pre.3ent.json')  as f:
        for line in f:
            tweets.append(json.loads(line))
        
        #load gold standard
        with open("preliminary_data/pre.3ent.tsv") as tsv:
            for line in csv.reader(tsv, dialect="excel-tab"):
                goldStandardSet[int((line[1]))] = line[2]
        
        for tweet in tweets:
            collection.append((tweet, goldStandardSet[tweet['id']]))

    return collection

###########################	 SUBROUTINES #########################
def tweet_features(tweet, all_words):
    tweet_words = set(tweet['text'])
    features = {}
    
    for word in all_words:
        
        features['contains %s' % word] = (word in tweet_words)
    features['favourites'] = tweet['favorite_count']
    features['retweets'] = tweet['retweet_count']
    return features

def cleanTweet(tweet):
    stemmer = nltk.stem.snowball.SnowballStemmer("english", ignore_stopwords=True)
    tokensArray = []
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(tweet['text'].lower())
    for token in tokens:
        token = stemmer.stem(token)
        
        if token not in stopwords.words('english') and token.isalpha():
            tokensArray.append(token)
    tweet['text'] = tokensArray
    return tweet

def generateVocabulary(tweets):
    vocab = []
    for(tweet, label) in tweets:
        for token in tweet['text']:
            print token
            vocab.append(token)
    freqDist = nltk.FreqDist(vocab)
    return freqDist
def setMinTermFrequency(words):
    newDictionary = {}
    for word in words:
        if words[word] > 2:
            newDictionary[word] = words[word]
            print "Added satisfiable term to dictionary"
    return newDictionary
####################### Main Routine ##########################
tweets = loadTweets()

tweets = [(cleanTweet(tweet), label) for (tweet, label) in tweets]
#use the middle 75 % of term frequency distribution
words = generateVocabulary(tweets)
print "Length of dictionary before processing: ", len(words)

all_words = setMinTermFrequency(words).keys()

print "Length of dictionary after processing: ", len(all_words)
featureSet = [(tweet_features(tweet, all_words), label) for (tweet, label) in tweets]

split = int(len(tweets)*0.503)
training_set = featureSet[:split]
test_set = featureSet[split:]


classifier = nltk.NaiveBayesClassifier.train(training_set)
####################### CLASSIFIER ANALYSIS ##########################
print "tweets: ", len(tweets)
print len(all_words)
print nltk.classify.accuracy(classifier, test_set)
classifier.show_most_informative_features()
####################### CLASSIFIER ANALYSIS ##########################
