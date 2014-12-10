#13/10/2014
#the script below takes in a json file of twitter objects and a file of the manual evaluation results.
# the output of the script is a collection of tuples that contain the tweet text and the reputation.

from pymongo import errors, MongoClient
import time
from bson.code import Code

#setup entitylist
client = MongoClient()
db = client.GTBT


collection = db.classifications

map = Code("function(){   var d = new Date(this.created_at); d.setMinutes(0); d.setHours(0); d.setSeconds(0); emit(d.getTime(), 1);}")
reduce = Code("function(key,values){return Array.sum(values)}")

result = collection.map_reduce(map, reduce, "TimeDistributions", query={"entity":"BMW"})

#calculate baseline
baseline = 0
for doc in result.find():
    baseline += doc['value']
baseline = baseline/result.find().count()
print baseline


time.sleep(180)


