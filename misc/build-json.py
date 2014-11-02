import json, csv
import redis
from pymongo import MongoClient
def buildCollection():
    
    tweets = []
    collection = []
    goldStandard = {}
    #load the tweets from the json file
    with open('preliminary_data/pre.3ent.json')  as f:
        for line in f:
            tweets.append(json.loads(line))
    
    #load the gold standard definitions into a dictonary for easy look up
    with open('preliminary_data/pre.3ent.tsv') as tsv:
        for line in csv.reader(tsv, dialect="excel-tab"):
            goldStandard[int((line[1]))] = (line[0],line[2])
    
    
    #finally, build the location into an array of elements as (JSON, dimension)
    for tweet in tweets:
        
        collection.append((goldStandard[tweet['id']][0],tweet, goldStandard[tweet['id']][1]))


    return collection

collection = buildCollection()
client = MongoClient()
classifications = client.GTBT.classifications
#build the json objects
for c in collection:
    c[1]['class'] = c[2]
    c[1]['entity'] = c[0]
    classifications.insert(c[1])