#handler for retrievint tweets about a specific entity
from pymongo import MongoClient, ASCENDING, DESCENDING
from tornado.web import RequestHandler, authenticated
from util.JsonEncoder import JSONEncoder
import json
class EntityHandler(RequestHandler):
    
    def get_current_user(self):
        return self.get_secure_cookie("user")
    
    @authenticated
    def get(self, entityid):
        client = MongoClient()
        
        #check entity is in the entity list
        if not client.gtbt.entities.find_one({"short": entityid}):
            self.redirect("/404/")
        
        
        #create a list of tweets
        classifications = client.gtbt.classifications
        results = classifications.find({"entity": entityid}).limit(10)
        
        tweets = []

        for c in results:
            tweets.append(json.loads(JSONEncoder().encode(c)))


        #create list of alerts
        alerts = client.gtbt.alerts
        alertsdbcursor = alerts.find({"entity": entityid}).limit(10)
        
        alerts = []
        for c in alertsdbcursor:
            alerts.append(json.loads(JSONEncoder().encode(c)))
        
        #check if this entity is currently being tracked
        isTracked = client.gtbt.tracks.find_one({"entity": entityid, "username":self.get_current_user()})

        #send response to client
        self.render("entity.html", tracked=isTracked, entity=entityid, tweets=tweets, alerts = alerts)