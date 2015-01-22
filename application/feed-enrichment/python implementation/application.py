#13/10/2014
#the script below takes in a json file of twitter objects and a file of the manual evaluation results.
# the output of the script is a collection of tuples that contain the tweet text and the reputation.
from Twitter4AP import TwitterRest
from pymongo import errors, MongoClient
import json, csv, nltk, time, random, requests
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

#setup entitylist
client = MongoClient()
db = client.GTBT
s = TwitterRest()
entityList = []



def loadTweets():
    tweets = []
    goldStandardSet = {}
    collection = []
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
    tweet_words = set(tweet['terms'])
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
        if token not in stopwords.words('english') and len(token) >2 and token.isalnum():
                tokensArray.append(token)
    tweet['terms'] = tokensArray
    return tweet

def generateVocabulary(tweets):
    vocab = []
    for(tweet, label) in tweets:
        for token in tweet['text']:
            vocab.append(token)
    freqDist = nltk.FreqDist(vocab)
    return freqDist
####################### Main Routine ##########################
tweets = loadTweets()
tweets = [(cleanTweet(tweet), label) for (tweet, label) in tweets]
#use the middle 75 % of term frequency distribution
words = generateVocabulary(tweets).keys()
all_words = words[:6000]
featureSet = [(tweet_features(tweet, all_words), label) for (tweet, label) in tweets]

split = int(len(tweets)*0.75)
training_set = featureSet[:split]
test_set = featureSet[split:]

classifier = nltk.NaiveBayesClassifier.train(training_set)
####################### CLASSIFIER ANALYSIS ##########################
print len(all_words)
print nltk.classify.accuracy(classifier, test_set)
####################### CLASSIFIER ANALYSIS ##########################


print 'Classifying...'
while True:
    
    db = client.gtbt.entities
    
    for e in db.find({"current":"True"}):
        result = TwitterRest().search({'q':e['short'], 'lang':'en'})
        statuses = json.loads(result.text)
        for status in statuses['statuses']:
            document = {}
            document['entity'] = e['short']
            
            document['gold'] = "False"
            document['tweet'] = status
        
            tweet = cleanTweet(status)
            label = classifier.classify(tweet_features(tweet, all_words))
            document['dimension'] = label
            print 'Tweet:', document['tweet']

            
            #add tweet to database using post request
            r = requests.post("http://localhost:8888/addtweet/", data=payload)
            
            with open("log.txt","a") as log:
                log.write(label + '\n')
    time.sleep(180)

