from pymongo import MongoClient
from util.JsonEncoder import JSONEncoder
from Handler import Handler
from bson.code import Code

class DistributionHandler(Handler):
    def get(self, entityid):
        #make sure the database connection is present before continuing.
        if self.classifications is None:
            self.send_error()
            return
        
        dimension=self.get_argument("class", None, True)
        
        #MapReduce Function definitions
        map = Code("function(){emit(this.place.country, 1);}")
        reduce = Code("function(key,values){return Array.sum(values)}")

        #The MapReduce Operation
        if dimension:
            result = self.classifications.map_reduce(map, reduce, "results",query={"place":{"$ne":None}, "entity":entityid, "class":dimension})
        else:
            result = self.classifications.map_reduce(map, reduce, "results",query={"place":{"$ne":None}, "entity":entityid})
        
        dist = {}
        for doc in result.find():
            dist[doc['_id']] = doc['value']
        
        response  = [('country', 'tweets')]+dist.items()
    
        self.set_header("Access-Control-Allow-Origin", "*")
        self.content_type = 'application/json'
        self.write(JSONEncoder().encode(response))