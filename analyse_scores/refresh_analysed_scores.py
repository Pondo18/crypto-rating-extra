import psycopg2

from utils import ConfigReader


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
    cursor.execute('REFRESH MATERIALIZED VIEW crypto_analysed_scores')
    conn.commit()
