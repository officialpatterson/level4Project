'''
    Author: Andrew R. Patterson
    Date:   14th June 2014
    Title:  setting up mongoDB with the Twitter stream
    Alt:    if connection to MongoDB instance cannot be established do *NOT* connect
    to Twitter stream.
    '''
import sys, os
from Twitter4AP import TwitterRest
from pymongo import errors
from pymongo import MongoClient
import json,time, csv
from time import gmtime, strftime

s = TwitterRest()
entityList = []
#setup entitylist
with open("entities.tsv") as tsv:
    for line in csv.reader(tsv, dialect="excel-tab"):
    entityList.append(line[0])

print "ENTITY LIST SETUP COMPLETE."

