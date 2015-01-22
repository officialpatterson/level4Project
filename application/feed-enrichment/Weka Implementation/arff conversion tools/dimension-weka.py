#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
#13/10/2014
#the script below takes in a json file of twitter objects and a file of the manual evaluation results.
# the output of the script is a collection of tuples that contain the tweet text and the reputation.
import json, csv, nltk, time, re
from pymongo import MongoClient



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

with open('txtfavrt.arff', 'w') as f:
    
    print(len(tweets))
    print("@RELATION tweets-test", file=f)
    print("@ATTRIBUTE text string", file=f)
    print("@ATTRIBUTE retweets numeric", file=f)
    print("@ATTRIBUTE favorites numeric", file=f)
    print("@ATTRIBUTE dimension {\"Undefined\", \"Governance\", \"Products & Services\", \"Performance\", \"Workplace\", \"Citizenship\", \"Innovation\", \"Leadership\"}", file=f)
    print("@data", file=f)
    for (tweet, label) in tweets:
        if label != "Undefined":
            escapedtext = tweet['text'].replace('"', r'').replace('\n', r'').replace('\r', r'')
            text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', escapedtext)
            print("\""+text+"\", "+str(tweet['favorite_count'])+", "+str(tweet['retweet_count'])+", "+"\""+label+"\"", file=f)