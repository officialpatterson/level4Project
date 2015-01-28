import twitter4j.Twitter;
import twitter4j.conf.ConfigurationBuilder;
import twitter4j.TwitterFactory;
import twitter4j.Query;
import twitter4j.QueryResult;
import twitter4j.Status;
import twitter4j.TwitterObjectFactory;
import com.mongodb.BasicDBObject;
import com.mongodb.BulkWriteOperation;
import com.mongodb.BulkWriteResult;
import com.mongodb.Cursor;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBCursor;
import com.mongodb.DBObject;
import com.mongodb.MongoClient;
import com.mongodb.ParallelScanOptions;
import org.json.JSONObject;
import com.mongodb.BasicDBObject;
import com.mongodb.util.JSON;

import java.util.ArrayList;
public class RetroEnrichment{
    
    
    public static void main(String[] args) throws Exception {
        
        TwitterCrawler tc = new TwitterCrawler();
        System.out.println("Created TC object");
        while(true){
            tc.updateEntities();
            tc.retrieve();
            
            
        }
        
    }


    
}