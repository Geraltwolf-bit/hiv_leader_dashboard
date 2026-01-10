import pandas as pd
import psycopg2
from psycopg2 import sql

db_params = {
    'host': 'localhost',
    'database': 'hiv_dashboard_db',
    'user': 'hiv_user',
    'password': '123',
    'port': '5433'
}

csv_path = 'hiv.csv'

table_name = 'sales'

def createtable(conn, cur):
    cur.execute("CREATE SCHEMA IF NOT EXISTS public;")
    cur.execute("SET search_path TO public;")
    create_table_query = sql.SQL("""
    CREATE TABLE IF NOT EXISTS {}(
    id SERIAL PRIMARY KEY,
    price DECIMAL,
    quantity INTEGER,
    date DATE,
    vendor VARCHAR(255),
    total DECIMAL);
    """).format(sql.Identifier(table_name))

    cur.execute(create_table_query)
    
    conn.commit()
    
    print(f"Table '{table_name}' created.")

def upload(conn, cur, csv_path):
    
    df = pd.read_csv(csv_path)
    
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    
    for index, row in df.iterrows():
        insert_query = sql.SQL("""
        INSERT INTO{}(
        price, quantity, date, vendor, total)
        VALUES(%s, %s, %s, %s, %s)
        """).format(sql.Identifier(table_name))

        cur.execute(insert_query,(
            row['price'],
            int(row['quantity']),
            row['date'],
            row['vendor'],
            row['total']
        ))

        conn.commit()

        print(f"Uploaded {len(df)} rows to {table_name}")

def main():
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        print('Connected to PostgreSQL')

        createtable(conn, cur)
        upload(conn, cur, csv_path)

        cur.close()
        conn.close()
    
    except Exception as e:
        print(f"error: {e}")

if __name__ == '__main__':
    main()