from pymongo import MongoClient
from util.JsonEncoder import JSONEncoder
from Handler import Handler

class EntityHandler(Handler):
    def get(self, entityid):
        #make sure the database connection is present before continuing.
        if self.classifications is None:
            self.send_error()
            return
        
        tweets = []
        class_aggregate = {}
        
        for c in self.classifications.find({"entity": entityid}):
            tweets.append(c)
            #if class already exists just increment the value  else create new class
            if c['class'] in class_aggregate:
                class_aggregate[c['class']] = class_aggregate[c['class']] + 1
            else:
                class_aggregate[c['class']] = 1
        
        if not class_aggregate:
            self.send_error(404)
            return
        
        response  = {'entityid':entityid, 'stats':class_aggregate, 'tweets':tweets}
        self.content_type = 'application/json'
        self.write(JSONEncoder().encode(response))