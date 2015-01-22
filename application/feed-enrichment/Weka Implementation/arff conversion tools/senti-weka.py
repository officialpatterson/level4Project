#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
#13/10/2014
#the script below takes in a json file of twitter objects and a file of the manual evaluation results.
# the output of the script is a collection of tuples that contain the tweet text and the reputation.
import json, csv, nltk, time, re
from pymongo import MongoClient



def loadTweets():
    
    goldStandardSet = {}
    collection = []
    
        
    #load gold standard
    with open("sentiment-gold-standard.csv", encoding='utf-8') as tsv:
        reader = csv.reader(tsv)
        next(reader, None)
        for line in reader:
            collection.append((line[0],line[1]))

    return collection

tweets = loadTweets()

with open('sentiment-text.arff', 'w') as f:
    
    print(len(tweets))
    print("@RELATION tweets-sentiment", file=f)
    print("@ATTRIBUTE text string", file=f)
    print("@ATTRIBUTE dimension {\"Positive\", \"Negative\"}", file=f)
    print("@data", file=f)
    counter = 0
    for (tweet, label) in tweets:
        escapedtext = tweet.replace('"', r'').replace('\n', r'').replace('\r', r'')
        text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', escapedtext)
            
        print("\""+text+"\", \""+label+"\"", file=f)