#handler for retrievint tweets about a specific entity
from pymongo import MongoClient, ASCENDING, DESCENDING
from tornado.web import RequestHandler, authenticated
from util.JsonEncoder import JSONEncoder
import json
class PinHandler(RequestHandler):
    
    def get_current_user(self):
        return self.get_secure_cookie("user")
    
    @authenticated
    def get(self):
        client = MongoClient()
        pins = client.gtbt.pins
        
        results = pins.find({"username": self.get_current_user()})
        pins = []
        for c in results:
            pins.append(c)
        self.render("pins.html", tweets=pins)