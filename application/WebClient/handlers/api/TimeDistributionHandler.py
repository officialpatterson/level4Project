from pymongo import MongoClient, ASCENDING
from util.JsonEncoder import JSONEncoder
from tornado.web import RequestHandler
from bson.code import Code
from datetime import datetime, timedelta, date
import urllib, collections, motor
from tornado import gen


class TimeDistributionHandler(RequestHandler):
    @gen.coroutine
    def get(self):
        
        #make sure the database connection is present before continuing.
        entityid = self.get_argument("entity", None)
        timeportion = self.get_argument("division", 24)
        start = int(self.get_argument("period", 365))
        dimension = self.get_argument("dimension", None)
        if(dimension):
            dimension = urllib.unquote(dimension)
        
        client = motor.MotorClient()
        classifications = client.gtbt.classifications
        
        start = datetime.now() - timedelta(days=start)
        end = datetime.now()
        
        #MapReduce Function definitions
        #need to find a way of converting the datetime to just a date object
    
        if timeportion == 24: #per day
            print "dividing by day"
            map = Code("function(){   var d = new Date(this.tweet.created_at); d.setHours(0); d.setMinutes(0);  d.setSeconds(0); emit(d.getTime(), 1);}")
        else: #per hour
            print "dividing by hour"
            map = Code("function(){   var d = new Date(this.tweet.created_at); d.setMinutes(0); d.setSeconds(0); emit(d.getTime(), 1);}")
        reduce = Code("function(key,values){return Array.sum(values)}")
        

        if entityid:
            if dimension:
                query={"entity":entityid, "dimension":dimension, "tweet":{"$ne":None},"tweet.created_at":{'$gte': start, '$lt': end}}
            else:
                query={"entity":entityid,"tweet":{"$ne":None},"tweet.created_at":{'$gte': start, '$lt': end}}
        else:
            query={"tweet":{"$ne":None},"tweet.created_at":{'$gte': start, '$lt': end}}


        result = classifications.inline_map_reduce(map, reduce, query=query)
        dist = collections.OrderedDict()
        
        documentset = yield result

        for doc in documentset:
            dist[doc['_id']] = doc['value']


    
        response  = [('time', 'count')]+dist.items()

        
        self.content_type = 'application/json'
        self.write(JSONEncoder().encode(response))

