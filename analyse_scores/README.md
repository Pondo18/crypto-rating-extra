# Analyse Score 
Das Verzeichnis analyse_scores dient dem Analysieren der einzeln post sentiment_scores.
Die sentiment_scores der einzelnen Posts werden nach CryptoCurrency grupiert für einzelne Tage zusammengefasst. 
Dadurch lässt sich der sentiment_score für den gesamten Tag darstellen. 
* * *

[analyse_all_scores.py](analyse_all_scores.py): 
- Sollte nur nach Initialisierung der DB ausgeführt werden.
- Erstellt einen Kombinierten sentiment_score für alle in der posts Tabelle referenzierten Tage 
  
[analyse_current_scores.py](analyse_current_scores.py): 
- Sollte in einem Cronjob jeden Tag ausgeführt werden
- Erstellt einen Kombinierten sentiment_score nur für den aktuellen Tag 