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
public class TwitterCrawler{
    
    MongoClient mongoClient;
    DB db;
    ArrayList<String> entities;
    Twitter twitter;
    
    public static void main(String[] args) throws Exception {
        
        TwitterCrawler tc = new TwitterCrawler();
        System.out.println("Created TC object");
        while(true){
            tc.updateEntities();
            tc.retrieve();
            
            
        }
        
    }
    public TwitterCrawler(){
        try{
            mongoClient = new MongoClient();
        }
        catch(Exception e){
            System.out.println("unable to connect to mongo database.");
        }
        db = mongoClient.getDB("gtbt");
        
        ConfigurationBuilder cb = new ConfigurationBuilder();
        cb.setJSONStoreEnabled(true);
        cb.setDebugEnabled(true)
        .setOAuthConsumerKey("gHCQjgvyCkjmOMAmJumLBvpCy")
        .setOAuthConsumerSecret("uZo6TmHwfzfcQDzMbTIu2f91EgUUjoQK82Lufq3zEFwWtADk9r")
        .setOAuthAccessToken("65512395-tPqnV4MiwJ0KbHsIc8KwkGUF1mYQ5xC3JQcv0WntF")
        .setOAuthAccessTokenSecret("ZypdVk89YTxRmUp7Icr0b0hDUZg2sRR8U2RbSavirwLJK");
        TwitterFactory tf = new TwitterFactory(cb.build());
        
        this.twitter = tf.getInstance();
        
    }

    public void updateEntities(){
        
        ArrayList<String> entityList = new ArrayList<String>();
        
        DBCollection entities = db.getCollection("entities");
        BasicDBObject q = new BasicDBObject("current", "True");
        DBCursor cursor = entities.find(q);
        try {
            while(cursor.hasNext()) {
                DBObject obj = cursor.next();
                
                String s = (String)obj.get("short");
                entityList.add(s);
            }
        } finally {
            cursor.close();
        }
        
        this.entities = entityList;
    }
    public void retrieve() throws Exception {
        
        DBCollection collection = db.getCollection("classifications");
        
        for(String entity: entities){
            Query query = new Query("lang:en "+entity);
            QueryResult result = twitter.search(query);
            System.out.println(entity);
            for (Status status : result.getTweets()) {
                String json = TwitterObjectFactory.getRawJSON(status);
                JSONObject t = new JSONObject(json);
                String text = t.getString("id_str");
                System.out.println(text);
                
                DBObject dbObject = (DBObject)JSON.parse(json);
                collection.insert(dbObject);
                
            }
            Thread.sleep(5000); //wait 2.5 minutes
        }
        
    }
    
}