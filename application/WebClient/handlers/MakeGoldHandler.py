#handler for retrievint tweets about a specific entity
from pymongo import MongoClient, ASCENDING, DESCENDING
from util.JsonEncoder import JSONEncoder
from tornado.web import RequestHandler
from bson.objectid import ObjectId

class MakeGoldHandler(RequestHandler):
    client = MongoClient()
    classifications = client.gtbt.classifications
    
    def get_current_user(self):
        return self.get_secure_cookie("user")
    
    def get(self):
        if not self.current_user:
            self.render("auth.html")
        else:
            self.clear_cookie("user")


    def post(self):
        tweetid = self.get_argument("id")
        #get tweet
        tweet = self.classifications.find_one({"_id":ObjectId(tweetid)})
        

        if tweet['gold'] == "True":
            print "pushing down"
            self.classifications.update({'_id':ObjectId(tweetid)}, {"$set": {"gold":"False"}}, upsert=False)
        if tweet['gold'] == "False":
            print "pushing up"
            self.classifications.update({'_id':ObjectId(tweetid)}, {"$set": {"gold":"True"}}, upsert=False)

