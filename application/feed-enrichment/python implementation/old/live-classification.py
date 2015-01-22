3#13/10/2014
#the script below takes in a json file of twitter objects and a file of the manual evaluation results.
# the output of the script is a collection of tuples that contain the tweet text and the reputation.
from Twitter4AP import TwitterRest
from pymongo import errors, MongoClient
import json, csv, nltk, time, random, requests
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import cPickle as pickle


###########################	 SUBROUTINES #########################
def loadTweets():
    
    tweets = []
    goldStandardSet = {}
    collection = []
    
    client = MongoClient()
    db = client.gtbt
    for document in db.classifications.find({"gold":"True"}):
        collection.append((document['tweet']['text'], document['dimension']))
    
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

def tweet_features(tweet, all_words):
    tweet_words = set(tweet)
    features = {}
    
    for word in all_words:
        features['contains %s' % word] = (word in tweet_words)
    return features

def cleanTweet(tweet):
    stemmer = nltk.stem.snowball.SnowballStemmer("english", ignore_stopwords=True)
    tokensArray = []
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(tweet.lower())
    for token in tokens:
        token = stemmer.stem(token)
        if token not in stopwords.words('english'):
            if len(token) >2:
                tokensArray.append(token)
    return tokensArray

def generateVocabulary(tweets):
    vocab = []
    for(tweet, label) in tweets:
        for token in tweet:
            vocab.append(token)
    freqDist = nltk.FreqDist(vocab)
    return freqDist
####################### Main Routine ##########################
classifier = None
tweets = loadTweets()
all_words = generateVocabulary(tweets).keys()



#setup entitylist
client = MongoClient()
db = client.gtbt
s = TwitterRest()

print 'Classifying...'
while True:
    for e in db.entities.find():
        result = s.search({'q':e['short'], 'lang':'en'})
        statuses = json.loads(result.text)

        for status in statuses['statuses']:
            if 'retweeted_status' in status:
                continue
        
            #classifiy tweet
            tweet = cleanTweet(status['text'])
            label = classifier.classify(tweet_features(tweet, all_words))
            
            document = {}
            document['entity'] = e['short'] #append the entity name to the tweet
            document['dimension'] = label
            document['tweet'] = status
            document['gold'] = "False"
            
            payload = {'tweet': json.dumps(document)}
            #add tweet to database using post request
            r = requests.post("http://localhost:8888/addtweet/", data=payload)
            with open("log.txt","a") as log:
                log.write(label + '\n')

        time.sleep(30)


