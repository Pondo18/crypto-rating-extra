# Query Reddit 
The directory queries and analyses reddit posts. Therefore, it uses the [Reddit-Api](https://www.reddit.com/dev/api/). 
The raw queried posts are getting persisted to the database. Furthermore, they are getting cleaned and analysed to compute a sentiment score.
Later on, this sentiment score is written in the database. 
* * *

[data_cleaning.py](data_cleaning.py): 
- Provides functionality necessary for the data cleaning
- called by query_reddit.py

[query_reddit.py](query_reddit.py)  :
- Should be run regularly as a Cronjob
- Searches new posts about the top 100 crypto_currencies, stored in the database
- Stores the posts in a raw format in the database
- Calls data_cleaning.py to clean those posts
- Computes and stores sentiment_score for each post  
