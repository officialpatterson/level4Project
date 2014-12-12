#handler for retrievint tweets about a specific entity
from pymongo import MongoClient, ASCENDING, DESCENDING
from util.JsonEncoder import JSONEncoder
from Handler import Handler
import json
#optional argyments: limit, time, dimension, start, end, retweetcount, favouritecount, followers
class PostTweet(Handler):
    def get(self):
        return
    
    def post(self):
        
        tweet = self.get_body_argument("tweet")
       
        self.classifications.insert(json.loads(tweet))