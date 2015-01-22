3#13/10/2014
#the script below takes in a json file of twitter objects and a file of the manual evaluation results.
# the output of the script is a collection of tuples that contain the tweet text and the reputation.
from Twitter4AP import TwitterRest
from pymongo import errors, MongoClient
import json, csv, nltk, time, random, requests
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer


client = MongoClient()
db = client.gtbt
collection = db.entities

#save in format {short: shortname, long:longname}
with open("entities.tsv") as tsv:
    for line in csv.reader(tsv, dialect="excel-tab"):
        print line[0], '\t', line[1]
        collection.insert({"short": line[0], "long":line[1], "current":"True"})

