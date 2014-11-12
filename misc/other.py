from nltk.classify import naivebayes
from nltk.corpus import stopwords
from nltk.tokenize import simple
import json, csv, string
def buildSet():
	tweets = []
	with open('preliminary_data/pre.3ent.json')  as f:
    		for line in f:
        		tweets.append(json.loads(line))

	goldStandardSet = {}
	collection = []
	#load gold standard
	with open("preliminary_data/pre.3ent.tsv") as tsv:
   		for line in csv.reader(tsv, dialect="excel-tab"):
			goldStandardSet[int((line[1]))] = line[2]
	
	for tweet in tweets:
		collection.append((tweet['text'], goldStandardSet[tweet['id']]))
	collection1 = []
	return collection


def features(tweet): #uses terms as features 
	features = {}
	termList = tweet.lower().split()
	stop = stopwords.words('english')
	
	for term in termList:
		if term not in stop and len(term) > 7:
			features['contains(%s)'% term] = term
	
	return features

def results(classifier, collection):
	#test the classifier
	correctLabels = 0
	incorrectLabels = 0	
	for tweet in collection[1024:]:

		expectedResult = tweet[1]
		actualResult = classifier.classify(features(tweet[0]))
		conf = classifier.prob_classify(features(tweet[0]))
		print 'E:',expectedResult, 'A:', actualResult
		print conf
		if actualResult == expectedResult:
			correctLabels +=1
		else:
			incorrectLabels +=1
	
	print '\n------------------Test Results------------------\n\n'
	print 'incorrect: ', incorrectLabels
	print 'correct: ', correctLabels
def run():
	collection = buildSet()
	trainingSet = []
	
	for (n,g) in collection[:1024]:
		featureSet = features(n)
		trainingSet.append((featureSet,g))
	
	classifier = naivebayes.NaiveBayesClassifier.train(trainingSet)
	results(classifier, collection)
	classifier.show_most_informative_features()
if __name__ == '__main__':
	run()
	
	print '\n------------------program terminated------------------\n\n'
