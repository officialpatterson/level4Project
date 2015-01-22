import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.File;
import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.classifiers.evaluation.NominalPrediction;
import weka.classifiers.rules.DecisionTable;
import weka.classifiers.rules.PART;
import weka.classifiers.trees.DecisionStump;
import weka.classifiers.trees.J48;
import weka.classifiers.trees.RandomForest;
import weka.classifiers.bayes.NaiveBayes;
import weka.classifiers.bayes.NaiveBayesMultinomial;
import weka.classifiers.bayes.NaiveBayesMultinomialText;
import weka.core.Instances;
import weka.core.stemmers.SnowballStemmer;
import weka.core.stopwords.WordsFromFile;
import weka.core.stopwords.*;
import weka.core.Stopwords;
import weka.core.converters.ArffLoader.ArffReader;
import weka.filters.*;
import weka.filters.unsupervised.attribute.*;
import weka.core.tokenizers.WordTokenizer;

public class TweetClassifier {
    public static BufferedReader readDataFile(String filename) {
        BufferedReader inputReader = null;
        
        try {
            inputReader = new BufferedReader(new FileReader(filename));
        } catch (FileNotFoundException ex) {
            System.err.println("File not found: " + filename);
        }
        
        return inputReader;
    }
    
    public static void main(String[] args) throws Exception {
        
        //load ARFF file
        System.out.print("Loading Data...");
        BufferedReader datafile = readDataFile("txtfavrt.arff");
        ArffReader arff = new ArffReader(datafile);
        
        Instances data = arff.getData();
        data.setClassIndex(data.numAttributes() - 1);
        
        System.out.println("...Done.");
        
        
        
        StringToWordVector filter = new StringToWordVector();
        filter.setInputFormat(data);
        
        filter.setTFTransform(true);
        
        //lower the document text case
        filter.setLowerCaseTokens(true);
        
        //use term frequencies
        filter.setMinTermFreq(2);
        
        filter.setOutputWordCounts(true);
        
        filter.setPeriodicPruning(-1.0);
        //apply stemming
        SnowballStemmer stemmer = new SnowballStemmer();
        filter.setStemmer(stemmer);
        
        filter.setStopwordsHandler(new Rainbow());
        
        //tokenize
        WordTokenizer tokenizer = new WordTokenizer();
        tokenizer.setDelimiters(".,;:\'\"()0123456789*-+`/@&}\\?!# ");
        filter.setTokenizer(tokenizer);
        
        filter.setWordsToKeep(300000);
        
        
       
        
        
        
        Instances dataFiltered = Filter.useFilter(data, filter);
        
        System.out.println("Tokenisation?\t"+filter.getTokenizer().getClass().getSimpleName());
        System.out.println("Stopwords?\t"+filter.getStopwordsHandler().getClass().getSimpleName());
        System.out.println("Stemming?\t"+filter.getStemmer().getClass().getSimpleName());
        
        
        //use PERCENTAGE Split
        int trainSize = (int) Math.round(dataFiltered .numInstances() * 0.75);
        int testSize = dataFiltered .numInstances() - trainSize;
        Instances train = new Instances(dataFiltered , 0, trainSize);
        Instances test = new Instances(dataFiltered , trainSize, testSize);
        
        //Instantiate new classifier
        Classifier classifier = new RandomForest();
        
        
        //train the classifier
        System.out.print("Building classifier model using "+classifier.getClass().getSimpleName()+"...");
        classifier.buildClassifier(train);
        System.out.println("...Done!");
        
        //Evaluate Classifier
        System.out.print("Evaluating...");
        Evaluation eval = new Evaluation(train);
        eval.evaluateModel(classifier, test);
        System.out.println("Complete!");
        
        //print results
        System.out.println(eval.toSummaryString());
        System.out.println("Weighted Precision:\t"+eval.weightedPrecision());
        
        
    }
}