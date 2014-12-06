#handler for retrievint tweets about a specific entity
from pymongo import MongoClient, ASCENDING, DESCENDING
from util.JsonEncoder import JSONEncoder
from Handler import Handler

#optional argyments: limit, time, dimension, start, end, retweetcount, favouritecount, followers
class TweetsHandler(Handler):
    def get(self, entityid):
        #make sure the database connection is present before continuing.
        if self.classifications is None:
            self.send_error()
            return
        
        tweets = []
        
        limit = int(self.get_argument("limit", 100, strip=False))
        time = self.get_argument("time", None, strip=False)
        retweetCount = self.get_argument("retweetcount", None, strip=False)
        favouriteCount = self.get_argument("favouritecount", None, strip=False)
       
       #Create query based on url parameters
        sort = []
        
        if time == "asc":
            sort.append(("time", ASCENDING))
        if time == "desc":
            sort.append(("time", DESCENDING))
        
        if retweetCount == "asc":
            sort.append(("retweet_count", ASCENDING))
        if retweetCount == "desc":
            sort.append(("retweet_count", DESCENDING))

        if favouriteCount == "asc":
            sort.append(("favourite_count", ASCENDING))
        if favouriteCount == "desc":
            sort.append(("favourite_count", DESCENDING))



        if(sort):
            queryResult = self.classifications.find({"entity": entityid}).sort(sort).limit(limit)
        else:
            queryResult = self.classifications.find({"entity": entityid}).limit(limit)
        
        
        for c in queryResult:
            tweets.append(c)
        
        
        response  = tweets
        self.set_header("Access-Control-Allow-Origin", "*")
        self.content_type = 'application/json'
        self.write(JSONEncoder().encode(response))