# Query Reddit 
Das Verzeichnis query_reddit dient der Abfrage und Analyse der einzelnen Posts.
Die abgefragten Beiträge werden in die Datenbanke eingetragen, gecleaned und analysiert.
Pro Beitrag wird ein Sentiment Score in der Datenbank hinterlegt.
* * *

[query_reddit/data_cleaning.py](data_cleaning.py): 
- Bietet Funktionen zum Datacleaning
- wird von query_reddit.py aufgerufen

[query_reddit/query_reddit.py](query_reddit.py)  :
- Sollte in einem Cronjob jeden Tag ausgeführt werden
- Fragt aktuell aktive Top Cryptos aus der DB ab
- Fragt neuste Beiträge aus ensprechenden Subreddits von Reddit-API ab
- Trägt die Beiträge in die DB ein
- Cleaned und analysiert die Beiträge
- Trägt den Sentiment_Score je post in die DB ein
