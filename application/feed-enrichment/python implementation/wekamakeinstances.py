#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
#13/10/2014
#the script below takes in a json file of twitter objects and a file of the manual evaluation results.
# the output of the script is a collection of tuples that contain the tweet text and the reputation.
import json, csv, nltk, time
from pymongo import errors, MongoClient




def loadTweets():
    
    tweets = []
    goldStandardSet = {}
    collection = []
    client = MongoClient()
    db = client.gtbt
    for doc in db.classifications.find({"gold":"True"}):
    
        collection.append((doc['tweet'], doc['dimension']))
    
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

tweets = loadTweets()

with open('data.txt', 'w') as f:
    print(len(tweets))
    for (tweet, label) in tweets:
        text = tweet['text'].replace('"', r'').replace('\n', r'')
       
        print("\""+text+"\","+"\""+label+"\"", file=f)