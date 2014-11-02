#Script for analysing the frequency distribution of the corpus
import json, csv
def buildCollection():
    
    tweets = []
    collection = []
    goldStandard = {}
    #load the tweets from the json file
    with open('preliminary_data/pre.3ent.json')  as f:
        for line in f:
            tweets.append(json.loads(line))
    
    #load the gold standard definitions into a dictonary for easy look up
    with open('preliminary_data/pre.3ent.tsv') as tsv:
        for line in csv.reader(tsv, dialect="excel-tab"):
            goldStandard[int((line[1]))] = line[2]
    
    
    #finally, build the location into an array of elements as (JSON, dimension)
    for tweet in tweets:
        collection.append((tweet, goldStandard[tweet['id']]))
    
    return collection

def loadDimensions():
    dimensions = {}
    with open('preliminary_data/pre.3ent.tsv') as tsv:
        for line in csv.reader(tsv, dialect="excel-tab"):
            if line[2] not in dimensions:
                dimensions[line[2]] = 0
            else:
                dimensions[line[2]] +=1
    return dimensions
def main():
    dimensions = loadDimensions()
    
    for d in dimensions:
        print d, ': ',dimensions[d]
    collection = buildCollection()


# my code here

if __name__ == "__main__":
    main()