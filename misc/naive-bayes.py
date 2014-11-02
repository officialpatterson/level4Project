#Implementation of Naive-bayes classifier using NLTK.
#16/10/2014
import json, csv, nltk
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
def naiveBayes():
    collection = buildCollection()
    
    #for each element in collection tokenize the string
    for i in range(0, len(collection)):
        tokenisedString = nltk.word_tokenize(collection[i][0]["text"])
        collection[i]= (tokenisedString, collection[i][1])

    print collection[i]
    return
def main():
    naiveBayes()
    return
# my code here

if __name__ == "__main__":
    main()