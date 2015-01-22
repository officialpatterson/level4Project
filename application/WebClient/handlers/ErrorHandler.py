#handler for retrievint tweets about a specific entity
from pymongo import MongoClient, ASCENDING, DESCENDING
from util.JsonEncoder import JSONEncoder
from tornado.web import RequestHandler, authenticated

class ErrorHandler(RequestHandler):
    
    def get_current_user(self):
        return self.get_secure_cookie("user")
    
    @authenticated
    def get(self):
        self.render("404.html")