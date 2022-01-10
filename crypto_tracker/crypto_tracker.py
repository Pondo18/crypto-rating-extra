from datetime import date

import requests
import psycopg2

from utils import ConfigReader


def get_top_cryptos():
    url = "http://data.messari.io/api/v2/assets?fields=id,slug,symbol,metrics/market_data/price_usd&limit=100"
    response = requests.request("get", url)
    return response.json().get('data')


def add_crypto_to_database(slug, symbol, rank, cursor):
    sql_query_insert = 'INSERT INTO crypto_currencies(symbol, slug, rank, active_top, last_changed) ' \
                       'VALUES (%s, %s, %s, TRUE, current_date) ' \
                       'ON CONFLICT (symbol) DO UPDATE SET rank=%s, active_top=true, last_changed=current_date '
    bind_data = (symbol, slug, rank, rank)
    cursor.execute(sql_query_insert, bind_data)


def set_old_cryptos(cursor):
    sql_query = 'UPDATE crypto_currencies SET active_top=false, rank=null WHERE NOT last_changed=%s'
    today = date.today()
    bind_data = (today,)
    cursor.execute(sql_query, bind_data)


def main():
    config_reader = ConfigReader()
    credentials = config_reader.config_variables
    conn = psycopg2.connect(
        host=credentials.get('host'),
        user=credentials.get('user'),
        password=credentials.get('password'),
        database=credentials.get('database')
    )
    cursor = conn.cursor()
    top_cryptocurrencies = get_top_cryptos()
    count = 1
    set_old_cryptos(cursor)
    for crypto_currency in top_cryptocurrencies:
        add_crypto_to_database(crypto_currency.get('slug'), crypto_currency.get('symbol'), count, cursor)
        count = count + 1
    conn.commit()
