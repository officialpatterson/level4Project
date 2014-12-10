from pymongo import MongoClient
from util.JsonEncoder import JSONEncoder
from Handler import Handler

class EntitiesHandler(Handler):
    def get(self):
        entities = self.classifications.distinct('entity')
        colsize = self.classifications.count()
        dimensions = self.classifications.distinct('class')
        response = {'size':colsize, 'entities': entities, 'dimensions': dimensions}
        self.set_header("Access-Control-Allow-Origin", "*") #Access control policy fix. remove in production.
        self.content_type = 'application/json'
        self.write(JSONEncoder().encode(response))

