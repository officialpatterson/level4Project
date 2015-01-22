#handler for retrievint tweets about a specific entity
from pymongo import MongoClient, ASCENDING, DESCENDING
from util.JsonEncoder import JSONEncoder
from tornado.web import RequestHandler
from bson.objectid import ObjectId
class PushPinHandler(RequestHandler):
    client = MongoClient()
    pins = client.gtbt.pins
    
    def get_current_user(self):
        return self.get_secure_cookie("user")
    
    def get(self):
        if not self.current_user:
            self.render("auth.html")
        else:
            self.clear_cookie("user")


    def post(self):
        tweetid = self.get_argument("id")
        
        #if already present remove from the pin
        pin = self.pins.find_one({"username":self.get_current_user(), "object._id":ObjectId(tweetid)})
        
        if pin:
            self.pins.remove({"username":self.get_current_user(), "object._id":ObjectId(tweetid)})
            print "pin removed"
        else:
            tweet = self.client.gtbt.classifications.find_one({"_id": ObjectId(tweetid)})
            self.pins.insert({"username":self.get_current_user(), "object":tweet})
            print "pin added"
