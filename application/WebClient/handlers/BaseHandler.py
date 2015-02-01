#handler for retrievint tweets about a specific entity
from pymongo import MongoClient, ASCENDING, DESCENDING
from tornado.web import RequestHandler, authenticated
from util.JsonEncoder import JSONEncoder
import json, motor
from bson import json_util
from datetime import datetime, timedelta, date
from tornado import gen

class EntityHandler(RequestHandler):
    
    client = motor.MotorClient()






