import psycopg2
import os

from utils import ConfigReader


def compute_analysed_scores_for_date(date):
    sql_query = 'SELECT AVG(sentiment_score), crypto_currency_id ' \
                'FROM reddit_posts p JOIN reddit_sentimentscores s ON p.id = s.post_id ' \
                'WHERE p.date=%s ' \
                'GROUP by crypto_currency_id'
    bind_data = (date,)
    cursor.execute(sql_query, bind_data)
    return cursor.fetchall()


def get_dates():
    sql_query = 'Select distinct date ' \
                'FROM reddit_posts'
    cursor.execute(sql_query)
    return cursor.fetchall()


def set_analysed_scores_for_date(date):
    analysed_scores = compute_analysed_scores_for_date(date)
    sql_query_insert = 'INSERT INTO crypto_analysedscores(date, crypto_currency_id, score) ' \
                       'VALUES (%s, %s, %s) '
    for analysed_score in analysed_scores:
        bind_data = (date, analysed_score[1], analysed_score[0])
        cursor.execute(sql_query_insert, bind_data)


def set_all_analysed_scores():
    dates = get_dates()
    for date in dates:
        set_analysed_scores_for_date(date)


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
    set_all_analysed_scores()
    conn.commit()
