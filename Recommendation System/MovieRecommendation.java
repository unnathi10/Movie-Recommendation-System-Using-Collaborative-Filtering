import java.io.File;
import java.io.IOException;
import java.util.List;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.mahout.cf.taste.common.TasteException;
import org.apache.mahout.cf.taste.eval.RecommenderBuilder;
import org.apache.mahout.cf.taste.eval.RecommenderEvaluator;
import org.apache.mahout.cf.taste.impl.common.LongPrimitiveIterator;
import org.apache.mahout.cf.taste.impl.eval.AverageAbsoluteDifferenceRecommenderEvaluator;
import org.apache.mahout.cf.taste.impl.model.file.FileDataModel;
import org.apache.mahout.cf.taste.impl.neighborhood.NearestNUserNeighborhood;
import org.apache.mahout.cf.taste.impl.recommender.GenericItemBasedRecommender;
import org.apache.mahout.cf.taste.impl.recommender.GenericUserBasedRecommender;
import org.apache.mahout.cf.taste.impl.similarity.LogLikelihoodSimilarity;
import org.apache.mahout.cf.taste.impl.similarity.PearsonCorrelationSimilarity;
import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.neighborhood.UserNeighborhood;
import org.apache.mahout.cf.taste.recommender.RecommendedItem;
import org.apache.mahout.cf.taste.recommender.Recommender;
import org.apache.mahout.cf.taste.recommender.UserBasedRecommender;
import org.apache.mahout.cf.taste.similarity.ItemSimilarity;
import org.apache.mahout.cf.taste.similarity.UserSimilarity;
import org.apache.mahout.common.RandomUtils;


public class itemRec {
	public static void main(String[] args) throws Exception
	{
		RandomUtils.useTestSeed();
		try{
			
		String INPUT_FILE =  "train.csv";
		String OUTPUT_FILE = "Itemrecommendations";
		
		// User Based
    	System.out.println("----User Based Recommendations----");
        final DataModel dm2 = new FileDataModel(new File(INPUT_FILE)); 
        
        RecommenderEvaluator evaluator = new AverageAbsoluteDifferenceRecommenderEvaluator();
        
        
        RecommenderBuilder builder = new RecommenderBuilder() {
      	  public Recommender buildRecommender(DataModel dataModel) throws TasteException {
      	    // build and return the Recommender to evaluate here
      		  UserSimilarity sim2 = new PearsonCorrelationSimilarity(dm2);
      	        
      	        UserNeighborhood neighborhood = new NearestNUserNeighborhood(4, sim2, dm2);
				
      	        return new GenericUserBasedRecommender(dm2, neighborhood, sim2);
      	  }
      };    
      UserBasedRecommender recommenderUser = (UserBasedRecommender) builder.buildRecommender(dm2);
        
        List<RecommendedItem> recomendations = recommenderUser.recommend(5, 5); // / recommend (user_id, number_of_items_to_recommend)
        long similarUsers[] = recommenderUser.mostSimilarUserIDs(5, 4);
        System.out.println("----5 User Based Recommendations for User 5-----"); 
        for (RecommendedItem recommendation : recomendations) {        	
            System.out.println(recommendation);    
        }
        System.out.println("-----4 Users similar to User 5-----"); 
        for (long userID : similarUsers) {        	
            System.out.println(userID);    
        }               
        
        double userScore = evaluator.evaluate(builder,null,dm2, 0.4, 1.0);
                
        String output = String.format("User Based Recommendations Score= %.2f", userScore);
        System.out.println(output);
        
        System.out.println("-----Item Based Recommendations for All Movies-----");
        
		DataModel dm = new FileDataModel(new File(INPUT_FILE));
		ItemSimilarity sim = new LogLikelihoodSimilarity(dm);
				
		GenericItemBasedRecommender recommender = new GenericItemBasedRecommender(dm, sim);            
		
		// Write Item Similarity scores to HDFS
		Configuration conf = new Configuration();
		
		FileSystem hdfs =FileSystem.get(conf);
		Path workingDir=hdfs.getWorkingDirectory();
				
		Path newFilePath=new Path(workingDir+"/"+OUTPUT_FILE);
		
		hdfs.createNewFile(newFilePath);
		
		FSDataOutputStream fsOutStream = hdfs.create(newFilePath);
		StringBuilder recoItems = new StringBuilder();
			
        for (LongPrimitiveIterator items = dm.getItemIDs(); items.hasNext();) {
            long itemId = items.nextLong();
            
            if(itemId!=0){
            	List<RecommendedItem> recommendations = recommender.mostSimilarItems(itemId, 5);
                
                for (RecommendedItem recommendation : recommendations) {
                	 
                	recoItems.append(itemId + "," + recommendation.getItemID() + "," + recommendation.getValue());
                	recoItems.append("\n");
                	System.out.println(itemId + "," + recommendation.getItemID() + "," + recommendation.getValue()); 
                	 
                }

            }
        }
        
            	byte[] byt=recoItems.toString().getBytes();
            	fsOutStream.write(byt); 
            	fsOutStream.close();   
        
        
    } catch (IOException e) {
        System.out.println("There was an error.");
        e.printStackTrace();
    } 
}
}
