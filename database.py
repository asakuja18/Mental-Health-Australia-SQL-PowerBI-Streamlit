import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def run_query(query):
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df