#13/10/2014
#the script below takes in a json file of twitter objects and a file of the manual evaluation results.
# the output of the script is a collection of tuples that contain the tweet text and the reputation.
import json, csv, nltk


###########################	 SUBROUTINE DEFINITIONS BELOW #########################
def loadTweets():
    tweets = []
    with open('preliminary_data/pre.3ent.json') as f:
        for line in f:
            tweets.append(json.loads(line))
    
	return tweets

def buildTrainingSet(tweets):
	goldStandardSet = {}
	collection = []
	#load gold standard
	with open("preliminary_data/pre.3ent.tsv") as tsv:
   		for line in csv.reader(tsv, dialect="excel-tab"):
			goldStandardSet[int((line[1]))] = line[2]
	
	for tweet in tweets:
		collection.append((tweet['text'].encode('utf8'), goldStandardSet[tweet['id']]))
	return collection

def get_words_in_tweets(tweets):
    all_words = []
    for (words, dimension) in tweets:
        all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

##################ALGORITHM CLASS########################
class NaiveBayes:

    def train():
        return

if __name__ == "__main__":
    dataset =  buildTrainingSet(loadTweets())
    print dataset[0][0]
    print extract_features(dataset[0][0])
