#13/10/2014
#for each vector compares against centroid vectors using cosine similarity. if similar according to threshold then add to cluster else create new cluster with vector as centroid. tweet can only be member of one cluster. (Single-pass clustering based on centroid similarity)
from pymongo import MongoClient
from documentpivot import DocumentPivot
from tools import *
if __name__ == "__main__":
  
    
    
    db = MongoClient().GTBT
    #load the tweets and tokenize & stem them

    topicDetector = DocumentPivot(0.7)
    for tweet in db.classifications.find():
        topicDetector.cluster(tweet)
    
    

    

    print 'number of clusters: ', len(clusters)







