from pymongo import MongoClient
from util.JsonEncoder import JSONEncoder
import tornado.escape
from tornado.web import RequestHandler

class DimensionDistributionHandler(RequestHandler):
    def get(self):

        entityid = self.get_argument("entity", None)
        
        if not entityid:
            self.send_error(404)
            return
        
        dimension_distribution = {}
        client = MongoClient()
        classifications = client.gtbt.classifications
        
        for c in classifications.find({"entity": entityid}):
            #if class already exists just increment the value  else create new class
            if 'dimension' in c and c['dimension'] in dimension_distribution:
                dimension_distribution[c['dimension']] = dimension_distribution[c['dimension']] + 1
            elif 'dimension' in c:
                dimension_distribution[c['dimension']] = 1
    
        response  = dimension_distribution
        self.content_type = 'application/json'
        self.write(JSONEncoder().encode(response))