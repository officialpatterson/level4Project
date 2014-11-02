from pymongo import MongoClient
from util.JsonEncoder import JSONEncoder
from Handler import Handler

class EntitiesHandler(Handler):
    def get(self):
        classifications = self.classifications.distinct('entity')
        self.set_header("Access-Control-Allow-Origin", "http://localhost:8000") #Access control policy fix. remove in production.
        self.content_type = 'application/json'
        self.write(JSONEncoder().encode(classifications))

