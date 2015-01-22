#handler for retrievint tweets about a specific entity
from pymongo import MongoClient, ASCENDING, DESCENDING
from util.JsonEncoder import JSONEncoder
from tornado.web import RequestHandler, authenticated
import json
class DashboardHandler(RequestHandler):
    
    def get_current_user(self):
        return self.get_secure_cookie("user")
    
    @authenticated
    def get(self):
        client = MongoClient()
        self.classifications = client.gtbt.classifications
        tracks = client.gtbt.tracks
        entities = client.gtbt.entities.distinct('short')

        numentities = len(client.gtbt.entities.distinct('short'))
        
        colsize = self.classifications.count()
        dimensions = len(self.classifications.distinct('dimension'))
        tracks = tracks.find({"username": self.get_current_user()}).distinct('entity')
        
        results = client.gtbt.alerts.find({"username":self.get_current_user()})
        alerts = []
        for c in results:
            alerts.append(json.loads(JSONEncoder().encode(c)))
        self.render("dashboard.html", dimensioncount=dimensions, entitycount=numentities, collectionsize=colsize, tracks=tracks, entities = entities, alerts=alerts, topics=None)