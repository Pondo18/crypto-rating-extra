import psycopg2

if __name__ == '__main__':
    conn = psycopg2.connect(
        host="10.11.12.116",
        database="postgres",
        user="root",
        password="pass")
    cursor = conn.cursor()
    cursor.execute('REFRESH MATERIALIZED VIEW crypto_analysed_scores')
    conn.commit()