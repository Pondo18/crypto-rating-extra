# Analyse Score 
The service analyses the sentiment scores to calculate an analysed_score for each cryptocurrency per day. 
Afterwards, those analysed_scores are persisted to a crypto_analysed_scores materialized view in the database.
* * *

[refresh_analysed_scores.py](refresh_analysed_scores.py): 
- Should be run regularly as a Cronjob
- Refreshes the crypto_analysed_scores materialized view

[analyse_all_scores.py (**Deprecated**)](analyse_all_scores.py): 
- Should be only run after system initialisation
- Creates a combined analysed_score for all the referenced days in the posts table grouped by cryptocurrency 
  
[analyse_current_scores.py (**Deprecated**)](analyse_current_scores.py): 
- Should be run regularly as a Cronjob
- Creates a combined analysed_score for the current day grouped by cryptocurrency 
