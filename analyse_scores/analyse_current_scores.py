import psycopg2

from utils import ConfigReader


def compute_analysed_scores():
    sql_query = 'SELECT AVG(sentiment_score), crypto_currency_id ' \
                'FROM reddit_posts p JOIN reddit_sentimentscores s ON p.id = s.post_id ' \
                'WHERE p.date=current_date-1 ' \
                'GROUP by crypto_currency_id'
    cursor.execute(sql_query)
    return cursor.fetchall()


def set_analysed_scores():
    analysed_scores = compute_analysed_scores()
    sql_query_insert = 'INSERT INTO crypto_analysedscores(date, crypto_currency_id, score) ' \
                       'VALUES (current_date-1, %s, %s) '
    for analysed_score in analysed_scores:
        bind_data = (analysed_score[1], analysed_score[0])
        cursor.execute(sql_query_insert, bind_data)


if __name__ == "__main__":
    config_reader = ConfigReader()
    credentials = config_reader.config_variables
    conn = psycopg2.connect(
        host=credentials.get('host'),
        user=credentials.get('user'),
        password=credentials.get('password'),
        database=credentials.get('database')
    )
    cursor = conn.cursor()
    set_analysed_scores()
    conn.commit()
