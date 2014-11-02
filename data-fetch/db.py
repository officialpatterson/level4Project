from Twitter4AP import TwitterRest
from pymongo import errors, MongoClient
import json,time, csv, sys, os

client = MongoClient()

db = client.twitter



s = TwitterRest()
entityList = []
#setup entitylist
with open("entities.tsv") as tsv:
    for line in csv.reader(tsv, dialect="excel-tab"):
        entityList.append(line[0])
while True:
    for e in entityList:
        result = s.search({'q':e})
        statuses = json.loads(result.text)
        for status in statuses['statuses']:
            status['entity'] = e #append the entity name to the tweet
            collection = db.tweets
            collection.insert(status)

    time.sleep(180)
print "ENTITY LIST SETUP COMPLETE."
print entityList
