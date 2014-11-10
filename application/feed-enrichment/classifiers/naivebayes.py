#13/10/2014
#Purpose: Create a (naive)bayesian probability model based on boolean features of an entity.
#No stempping, tokenized only on spaces.
#only uses the x most common words in the collection as possibile features
import nltk, json, csv, random
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
###########################	 LOADING DATA #########################

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
        if goldStandardSet[tweet['id']] in labelCount:
            labelCount[goldStandardSet[tweet['id']]] = labelCount[goldStandardSet[tweet['id']]] + 1
        else:
            labelCount[goldStandardSet[tweet['id']]] = 1
    print 'labels: '
    print labelCount
    print 'end'
    return collection

###########################	 SUBROUTINES #########################
def tweet_features(tweet, all_words):
    tweet_words = set(tweet)
    features = {}
    
    for word in all_words:
        features['contains %s' % word] = (word in tweet_words)
    return features

def tokenizedTweets(tweets):
    stemmer = nltk.stem.snowball.SnowballStemmer("english", ignore_stopwords=True)
    #for each tweet tokenize, remove stop words and stem
    for i in range(0, len(tweets)):
        tokensArray = []
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(tweets[i][0].lower())
        for token in tokens:
            token = stemmer.stem(token)
            if token not in stopwords.words('english'):
                
                if len(token) >2:
                    tokensArray.append(token)
    
        label = tweets[i][1]
        tweets[i]= (tokensArray, label)
    return tweets

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
tweets = loadTweets()
random.shuffle(tweets)
tweets = [(cleanTweet(tweet), label) for (tweet, label) in tweets]
all_words = generateVocabulary(tweets).keys()
featureSet = [(tweet_features(tweet, all_words), label) for (tweet, label) in tweets]

training_set = featureSet[:2020]
test_set = featureSet[2020:]

classifier = nltk.NaiveBayesClassifier.train(training_set)
####################### CLASSIFIER ANALYSIS ##########################
print nltk.classify.accurracy(classifier, test_set)
####################### LIVE CLASSIFICATION ##########################


