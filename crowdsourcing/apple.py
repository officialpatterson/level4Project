#13/10/2014
#the script below searches for the entity named apple and stores it in the collection
from Twitter4AP import TwitterRest
from pymongo import errors, MongoClient
import json, csv, nltk, time

#setup entitylist
client = MongoClient()
db = client.GTBT
s = TwitterRest()
entityList = []

while True:
    result = s.search({'q':'apple', 'lang':'en'})
    statuses = json.loads(result.text)
    for status in statuses['statuses']:
        collection = db.apple
        collection.insert(status)
    time.sleep(180)


