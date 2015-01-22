import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.ArrayList;
import org.json.*;

public class lineread{
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
        
        BufferedReader dimensionFile = readDataFile("preliminary_data/pre.3ent.tsv");
        while (dimensionFile.ready()) {
            String s = dimensionFile.readLine();
            String[] portions = s.split("\t");
            String tweetID = portions[1];
            String dimension = portions[2];
            
        }
        ArrayList<String> tweets = new ArrayList<String>();
        BufferedReader tweetsFile = readDataFile("preliminary_data/pre.3ent.json");
        
        while (tweetsFile.ready()) {
            String s = tweetsFile.readLine();
            tweets.add(s);
            
        }

        JSONObject obj = new JSONObject(tweets.get(0));
        String pageName = obj.getString("text");
        
        System.out.println(pageName);
    }
}