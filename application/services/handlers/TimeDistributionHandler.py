from pymongo import MongoClient
from util.JsonEncoder import JSONEncoder
from Handler import Handler
from bson.code import Code
import datetime

class TimeDistributionHandler(Handler):
    def get(self, entityid):
        #make sure the database connection is present before continuing.
        if self.classifications is None:
            self.send_error()
            return
    
        dimension=self.get_argument("class", None, True)
        
        #MapReduce Function definitions
        #need to find a way of converting the datetime to just a date object
        map = Code("function(){   var d = new Date(this.created_at); d.setMinutes(0); d.setHours(0); d.setSeconds(0); emit(d.getTime(), 1);}")
        reduce = Code("function(key,values){return Array.sum(values)}")
        
       
        result = self.classifications.map_reduce(map, reduce, "TimeDistributions", query={"entity":entityid})
        dist = {}
        for doc in result.find():
            dist[doc['_id']] = doc['value']
        
        response  = [('time', 'count')]+dist.items()
     
        self.set_header("Access-Control-Allow-Origin", "*")
        self.content_type = 'application/json'
        self.write(JSONEncoder().encode(response))