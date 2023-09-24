import psycopg2
from sqlalchemy import create_engine

from scraper import to_write

# postgres table creation
conn_string = 'postgresql://postgres:postgres@localhost:5432/postgres'

conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
  
table_schema = """
    DROP TABLE IF EXISTS properties;
    CREATE TABLE properties (
        index int PRIMARY KEY,
        name VARCHAR (255),
        photo VARCHAR (255));
"""

cursor.execute(table_schema)
conn.commit()

# insert the data
db = create_engine(conn_string)
conn = db.connect()

to_write.to_sql('properties', con=conn, if_exists='replace',index=False)

conn.close()

# Define a function to fetch data from the PostgreSQL database
def fetch_data_from_postgres():
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()

        # Change this query to match your table structure
        query = "SELECT * FROM properties"
        cursor.execute(query)

        # Fetch all rows as a list of dictionaries
        rows = cursor.fetchall()
        data = [{'index': row[0], 'title': row[1], 'link': row[2]} for row in rows]

        cursor.close()
        conn.close()

        return data

    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL:", e)
        return []