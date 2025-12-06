import os
from dotenv import load_dotenv
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

# ---  Load settings ---
def load_settings():
    load_dotenv()
    return {
        "user": os.getenv("SNOWFLAKE_USER"),
        "password": os.getenv("SNOWFLAKE_PASSWORD"),
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
        "database": os.getenv("SNOWFLAKE_DATABASE"),
        "schema": os.getenv("SNOWFLAKE_SCHEMA"),
        "csv_file": os.getenv("CSV_FILE"),
        "table_name": os.getenv("TABLE_NAME")
    }

# --- Connect to Snowflake ---
def connect_to_snowflake(settings):
    conn = snowflake.connector.connect(
        user=settings["user"],
        password=settings["password"],
        account=settings["account"],
        warehouse=settings["warehouse"],
        database=settings["database"],
        schema=settings["schema"]
    )
    return conn, conn.cursor()

# ---  Create table if not exists ---
def create_table(cur, table_name):
    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        patient_id INT,
        first_name STRING,
        last_name STRING,
        birth_date DATE,
        gender STRING,
        diagnosis STRING,
        visit_date DATE,
        treatment STRING,
        cost FLOAT
    )
    """)

# --- Upload CSV DataFrame ---
def upload_csv(df, conn, table_name):
    success, nchunks, nrows, _ = write_pandas(conn, df, table_name.upper())
    return success, nchunks, nrows

# --- Query table ---
def query_table(cur, query):
    cur.execute(query)
    return cur.fetchall()
