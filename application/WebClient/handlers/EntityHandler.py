#handler for retrievint tweets about a specific entity
from pymongo import MongoClient, ASCENDING, DESCENDING
from tornado.web import RequestHandler, authenticated
from util.JsonEncoder import JSONEncoder
import json, motor
from bson import json_util
from datetime import datetime, timedelta, date
from tornado import gen

class EntityHandler(RequestHandler):
    
    def get_current_user(self):
        return self.get_secure_cookie("user")
    
    @gen.coroutine
    @authenticated
    def get(self, entityid):
        client = motor.MotorClient()
        
        #check entity is in the entity list
        if not (yield client.gtbt.entities.find_one({"short": entityid})):
            self.redirect("/404/")
        
        
        #create a list of tweets
        start = datetime.now() - timedelta(days=int(self.get_argument("timeperiod", 365)))
        end = datetime.now()
       
       
        cursor = client.gtbt.classifications.find({"entity": entityid, "tweet.created_at":{'$gte': start, '$lt': end}}).limit(10)
        tweets = []
        
        while (yield cursor.fetch_next):
            tweets.append(cursor.next_object())


        #create list of alerts
        alertsdbcursor = client.gtbt.alerts.find({"entity": entityid}).limit(10)
        alerts = []
        
        while (yield alertsdbcursor.fetch_next):
            alerts.append(alertsdbcursor.next_object())
        
        #check if this entity is currently being tracked
        isTracked = yield client.gtbt.tracks.find_one({"entity": entityid, "username":self.get_current_user()})

        #send response to client
        self.render("entity.html", tracked=isTracked, entity=entityid, tweets=tweets, alerts=alerts, timeperiod=self.get_argument("timeperiod", 365))





