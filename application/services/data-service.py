#Application code for Delivering partial REST service of GTBT data
#30/10/2014 19:00
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url
from pymongo import MongoClient
import pymongo
from util.JsonEncoder import JSONEncoder
from handlers.EntityHandler import EntityHandler
from handlers.EntitiesHandler import EntitiesHandler


app = Application([
                   url(r"/entity/([A-Za-z0-9]+)", EntityHandler), #IMPLEMENT THIS IMMEDIATELY
                    url(r"/entities/", EntitiesHandler),
                   ])

def startService():
    app.listen(8888)
    print 'Rest service started. Listening on port 8888.'
    try:
        IOLoop.instance().start()
    except:
        IOLoop.instance().stop()
        print '\nREST SERVICE STOPPED\nTornado Server shutdown'

if __name__ == "__main__":
    startService()


