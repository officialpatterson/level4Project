#anything applied in this file affects all requsts for the service.
from tornado.web import RequestHandler
from pymongo import MongoClient

class Handler(RequestHandler):
    def initialize(self):
        client = MongoClient()
        self.classifications = client.GTBT.classifications
        self.set_header("Access-Control-Allow-Origin", "*")


