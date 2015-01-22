#helper functions for taking tweets from the database and preparing them for classification & clustering
from pymongo import MongoClient
import nltk, math
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from collections import Counter

def loadTweets(entity, dimension):
    
    db = MongoClient().GTBT
    collection = []
    
    [collection.append(e) for e in db.classifications.find({"entity":entity, "class":dimension})]

    return collection

###########################	 SUBROUTINES #########################
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
    return Counter(tokensArray)

def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    
    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    
    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

