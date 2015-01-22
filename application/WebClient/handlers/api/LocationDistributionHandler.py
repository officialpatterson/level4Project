from pymongo import MongoClient
from util.JsonEncoder import JSONEncoder
from bson.code import Code
from tornado.web import RequestHandler

class LocationDistributionHandler(RequestHandler):
    def get(self):
        
        entityid = self.get_argument("entity", None)
        
        if not entityid:
            self.send_error(404)
            return
        
        client = MongoClient()
        classifications = client.gtbt.classifications
        
        dimension=self.get_argument("dimension", None, True)
        
        #MapReduce Function definitions
        map = Code("function(){emit(this.tweet.place.country, 1);}")
        reduce = Code("function(key,values){return Array.sum(values)}")

        #The MapReduce Operation
        if dimension:
            result = classifications.map_reduce(map, reduce, "results",query={"tweet.place":{"$ne":None}, "entity":entityid, "dimension":dimension})
        else:
            result = classifications.map_reduce(map, reduce, "results",query={"tweet.place":{"$ne":None}, "entity":entityid})
        
        dist = {}
        for doc in result.find():
            dist[doc['_id']] = doc['value']
        
        response  = [('country', 'tweets')]+dist.items()
    
        self.set_header("Access-Control-Allow-Origin", "*")
        self.content_type = 'application/json'
        self.write(JSONEncoder().encode(response))