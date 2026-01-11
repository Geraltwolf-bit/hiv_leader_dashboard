import pandas as pd
import psycopg2
import os
import glob
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

def import_excel():
    database_url = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(database_url)

    excel_files = glob.glob('*.xlsx')

    if not excel_files:
        print("No excel files found")
        return

    print(f" Found {len(excel_files)} excel files")

    for file_path in excel_files:
        filename = os.path.basename(file_path)
        table_name = os.path.splitext(filename)[0]

        print(f"Processing: {filename}")
        print(f"Table name: {table_name}")

        try:
            cur = conn.cursor()
            df = pd.read_excel(file_path, engine = 'openpyxl')
            print(f"rows: {len(df)}, columns: {len(df.columns)}")

            if 'id' in df.columns:
                df = df.drop(columns=['id'])

            df.columns = [str(col).strip().lower().replace(' ', '_') for col in df.columns]

            create_columns = []
            for col in df.columns:
                dtype = str(df[col].dtype)
                if 'int' in dtype:
                    pg_type = 'INTEGER'
                elif 'float' in dtype:
                    pg_type = 'DECIMAL(10, 2)'
                elif 'date' in dtype:
                    pg_type = 'DATE'
                else:
                    pg_type = 'VARCHAR(255)'

                create_columns.append(f"{col} {pg_type}")
            
            cur.execute(sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(table_name)))

            create_sql = sql.SQL("CREATE TABLE {} (id SERIAL PRIMARY KEY, {})").format(sql.Identifier(table_name),
            sql.SQL(", ").join([sql.SQL(col) for col in create_columns]))

            cur.execute(create_sql)

            for _, row in df.iterrows():
                columns = ', '.join(df.columns)
                placeholders = ', '.join(['%s'] * len(df.columns))

                insert_sql = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                    sql.Identifier(table_name),
                    sql.SQL(columns),
                    sql.SQL(placeholders)
                )

                cur.execute(insert_sql, tuple(row))

            conn.commit()
            cur.close()

        except Exception as e:
            print(f"Error {e}")

    conn.close()

if __name__ == '__main__':
    import_excel()