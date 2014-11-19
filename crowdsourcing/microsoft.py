#13/10/2014
#the script below searches for the entity named apple and stores it in the collection
from Twitter4AP import TwitterRest
from pymongo import errors, MongoClient
import json, csv, nltk, time

#setup entitylist
s = TwitterRest()
entityList = ['microsoft','apple','hsbc', 'facebook', 'google', 'ford', 'twitter', 'jp morgan', 'samsung' 'huawei']

#authenticate Database Connection
connection = MongoClient("ds041157.mongolab.com", 41157)
db = connection["gtbt"]
# MongoLab has user authentication
db.authenticate("officialandyp", "cockatiel93")
while True:
    for e in entityList:
        result = s.search({'q':e, 'lang':'en'})
        statuses = json.loads(result.text)
        for status in statuses['statuses']:
	    status['entity'] = e
            collection = db.tweets
	    try:
                collection.insert(status)
	    except errors.DuplicateKeyError:
		print 'err'
    time.sleep(120)
