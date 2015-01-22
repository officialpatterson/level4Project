import csv, json, sys, os, time
from pymongo import errors, MongoClient
from Twitter4AP import TwitterRest

client = MongoClient()
db = client.gtbt
collection = db.classifications



def chunks(l, n):
    """ Yield n successive chunks from l.
        """
    newn = int(len(l) / n)
    for i in xrange(0, n-1):
        yield l[i*newn:i*newn+newn]
    yield l[n*newn-newn:]



#open the file and retrieve a tuple (id, dimension)
tweetIDList = []
tweetDict = {}
s = TwitterRest()

with open('gs.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        tweetIDList.append(row['id_str'])
        tweetDict[row['id_str']] = row['text']



portions = chunks(tweetIDList, 25)


#go through each portion and perform a twitter request on it
while True:
    ids = portions.next()
    args = ','.join(map(str, ids))
 
    result = s.getTweets({"id":args})
    
    print result.status_code
    if result.status_code != 200:
        print result.text
        break
    tweets = json.loads(result.text)

    for tweet in tweets:
        document = {}
        document['entity'] = "BMW"
        document['dimension'] = tweetDict[tweet['id_str']]
        document['gold'] = "True"
        document['tweet'] = tweet
        #collection.insert(document)
        print "ID: ", tweet['id_str'], " text: ", tweet['text']
    










