from pymongo import MongoClient
from util.JsonEncoder import JSONEncoder
import tornado.escape
from tornado.web import RequestHandler
from datetime import datetime, timedelta, date
from tornado import gen
import motor

class DimensionDistributionHandler(RequestHandler):
    
    @gen.coroutine
    def get(self):

        entityid = self.get_argument("entity", None)
        start = int(self.get_argument("period", 365))
        if not entityid:
            self.send_error(404)
            return
        
        dimension_distribution = {}
        client = motor.MotorClient()
        
        classifications = client.gtbt.classifications
        
        start = datetime.now() - timedelta(days=start)
        end = datetime.now()
    
        cursor = classifications.find({"entity": entityid, "tweet.created_at":{'$gte': start, '$lt': end}})
        while (yield cursor.fetch_next):
            c = cursor.next_object()

            if 'dimension' in c and c['dimension'] in dimension_distribution:
                dimension_distribution[c['dimension']] = dimension_distribution[c['dimension']] + 1
            elif 'dimension' in c:
                dimension_distribution[c['dimension']] = 1

        response  = dimension_distribution
        self.content_type = 'application/json'
        self.write(JSONEncoder().encode(response))

