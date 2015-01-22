#handler for retrievint tweets about a specific entity
from pymongo import MongoClient, ASCENDING, DESCENDING
from util.JsonEncoder import JSONEncoder
from tornado.web import RequestHandler, authenticated

class DiscoverHandler(RequestHandler):
    
    def get_current_user(self):
        return self.get_secure_cookie("user")
    
    @authenticated
    def get(self):
        client = MongoClient()
  
        entities = client.gtbt.classifications.distinct('entity')

        
     
        self.render("discover.html", entities = entities)