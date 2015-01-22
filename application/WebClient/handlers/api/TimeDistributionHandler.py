from pymongo import MongoClient
from util.JsonEncoder import JSONEncoder
from tornado.web import RequestHandler
from bson.code import Code
import datetime

class TimeDistributionHandler(RequestHandler):
    def get(self):
        
        #make sure the database connection is present before continuing.
        entityid = self.get_argument("entity", None)
        timeportion = self.get_argument("division", 24)
        if not entityid:
            self.send_error(404)
            return
        
        client = MongoClient()
        classifications = client.gtbt.classifications
        
        
        #MapReduce Function definitions
        #need to find a way of converting the datetime to just a date object
        
        if timeportion == 24:
            map = Code("function(){   var d = new Date(this.tweet.created_at); d.setMinutes(0); d.setHours(0); d.setSeconds(0); emit(d.getTime(), 1);}")
        reduce = Code("function(key,values){return Array.sum(values)}")
        
       
        result = classifications.map_reduce(map, reduce, "TimeDistributions", query={"entity":entityid,"tweet":{"$ne":None}})
        
        dist = {}
        for doc in result.find():
            dist[doc['_id']] = doc['value']
        
        response  = [('time', 'count')]+dist.items()
    
        self.content_type = 'application/json'
        self.write(JSONEncoder().encode(response))