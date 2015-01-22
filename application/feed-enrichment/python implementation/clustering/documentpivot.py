#30th December 2014
#Andrew R. Patterson
#class specification for adding tweets to clusters based on similarity threshold specified on object construction. Also, documents can have belong to multiple clusters (overlap).
from tools import *

class DocumentPivot():
    
    sthreshold = None
    
    def __init__(self, threshold):
        
        if threshold < 0 or threshold > 1:
            return None #return empty object as threshold
        
        
        self.threshold = threshold

    def getClusters(self,document): #returns a list of clusters(id, centroid) that share the same entity and dimension
        db = MongoClient().GTBT
        clusters = []
        [clusters.append((e['_id'],e['centroid'])) for e in db.clusters.find({"entity":document['entity'], "dimension":document['class']})]
    
        return clusters
    
    def updateCluster(self,clusterid, document):
        print 'update', clusterid
        db = MongoClient().GTBT
        db.clusters.update({" _id": clusterid},{ "$push": { "tweets": document } })
    
    def createCluster(self, document):
        print 'new'
        db = MongoClient().GTBT
        db.clusters.insert({"centroid":document, "entity":document['entity'], "dimension":document['class'], "tweets":[document]})
    
    def cluster(self, document):
        
        clusters = self.getClusters(document)
        #convert document to vector
        
        if not clusters:
            self.createCluster(document)
        else:
            isAdded = False
            v = cleanTweet(document['text'])
            
            for centroid in clusters:
                centroidVector = cleanTweet(centroid[1]['text'])
                
                if get_cosine(centroidVector, v) >= self.threshold:
                    isAdded = True
                    self.updateCluster(centroid[0], document)
            if not isAdded:
                self.createCluster(document)


