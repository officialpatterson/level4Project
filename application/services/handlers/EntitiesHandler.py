from tornado.web import RequestHandler
from pymongo import MongoClient
from util.JsonEncoder import JSONEncoder
class EntitiesHandler(RequestHandler):
    def initialize(self):
        client = MongoClient()
        self.classifications = client.GTBT.classifications
    def get(self):
        classifications = self.classifications.distinct('entity')
        self.set_header("Access-Control-Allow-Origin", "http://localhost:8000") #Access control policy fix. remove in production.
        self.content_type = 'application/json'
        self.write(JSONEncoder().encode(classifications))

