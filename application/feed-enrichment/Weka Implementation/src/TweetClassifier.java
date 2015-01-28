/*using Naive Bayes Algorithm to classify into 7 dimensions (Undefined has been removed)
    1. remove urls
    2. lower case
    3. tokenize on non-alphabetic characters
    4. stem/remove stopwords
    5. remove terms with TF<2
    6. output word counts, vector=[0,2,3,1,1,1,10]
 */
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.File;
import java.util.Random;
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
import weka.core.Instance;
import weka.core.Attribute;
import weka.core.stemmers.SnowballStemmer;
import weka.core.stopwords.WordsFromFile;
import weka.core.stopwords.*;
import weka.core.Stopwords;
import weka.core.converters.ArffLoader.ArffReader;
import weka.filters.*;
import weka.filters.unsupervised.attribute.*;
import weka.core.tokenizers.WordTokenizer;

public class TweetClassifier {
    
    Filter filter;
    Classifier classifier;
    
    public static BufferedReader readDataFile(String filename) {
        BufferedReader inputReader = null;
        
        try {
            inputReader = new BufferedReader(new FileReader(filename));
        } catch (FileNotFoundException ex) {
            System.err.println("File not found: " + filename);
        }
        
        return inputReader;
    }
    public static Filter createFilter(){
        StringToWordVector filter = new StringToWordVector();
        
        //lower the document text case
        filter.setLowerCaseTokens(true);
        
        filter.setOutputWordCounts(true);
        
        //tokenize
        WordTokenizer tokenizer = new WordTokenizer();
        tokenizer.setDelimiters(".,;:\'\"()0123456789*-+`/@&}\\?!# ");
        filter.setTokenizer(tokenizer);

        
        filter.setMinTermFreq(2);
        
        filter.setPeriodicPruning(-1.0);
        
        //apply stemming
        SnowballStemmer stemmer = new SnowballStemmer();
        filter.setStemmer(stemmer);
        
        filter.setStopwordsHandler(new Rainbow());
        
        
        
     
        
        return filter;
    }
    public TweetClassifier() throws Exception{
        
        //load ARFF file
        System.out.print("Loading Data...");
        BufferedReader datafile = readDataFile("data/txtfavrt70.arff");
        ArffReader arff = new ArffReader(datafile);
        
        Instances data = arff.getData();
        data.setClassIndex(data.numAttributes() - 1);
        
        System.out.println("...Done.");
        
        filter = TweetClassifier.createFilter();
        filter.setInputFormat(data);
        Instances dataFiltered = Filter.useFilter(data, filter);
        
        
        /*instantiate classifier*/
        classifier = new RandomForest();
        classifier.buildClassifier(dataFiltered);
        
        //Evaluate Classifier
        System.out.print("Evaluating...");
        Evaluation eval = new Evaluation(dataFiltered);
        eval.crossValidateModel(classifier, dataFiltered, 10, new Random(1));
        System.out.println("Complete!");
        
        
        System.out.println("Percent correct: "+ Double.toString(eval.pctCorrect()));
        
    }
    public String classify(){
        return null;
    }
    public static void main(String[] args) throws Exception {
        
        
        TweetClassifier tc = new TweetClassifier();
        
        
    }
}