#handler for retrievint tweets about a specific entity
from pymongo import MongoClient, ASCENDING, DESCENDING
from util.JsonEncoder import JSONEncoder
from tornado.web import RequestHandler, authenticated

class TrackHandler(RequestHandler):
    client = MongoClient()
    entities = client.gtbt.entities
    tracks = client.gtbt.tracks
    
    def get_current_user(self):
        return self.get_secure_cookie("user")
    
    @authenticated
    def get(self):
        self.render("trackentity.html")
    
    @authenticated
    def post(self):
        entityname = self.get_argument("entity")

        entity = self.entities.find_one({"short":entityname})

        if not entity:
            self.entities.insert({"short":entityname})

        self.tracks.insert({"username":self.get_current_user(), "entity":entityname})
        self.redirect("/dashboard/")