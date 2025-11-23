import os
from dotenv import load_dotenv
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

# ---  Load settings ---
def load_settings():
    load_dotenv()
    settings = {
        "user": os.getenv("SNOWFLAKE_USER"),
        "password": os.getenv("SNOWFLAKE_PASSWORD"),
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
        "database": os.getenv("SNOWFLAKE_DATABASE"),
        "schema": os.getenv("SNOWFLAKE_SCHEMA"),
        "csv_file": os.getenv("CSV_FILE"),
        "table_name": os.getenv("TABLE_NAME")
    }
    return settings

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

# ---  Upload CSV DataFrame using write_pandas ---
def upload_csv(df, conn, table_name):
    success, nchunks, nrows, _ = write_pandas(conn, df, table_name.upper())
    print(f"Upload success: {success}, rows: {nrows}, chunks: {nchunks}")

# ---  Query table to verify ---
def query_table(cur, table_name, limit=10):
    cur.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
    results = cur.fetchall()
    print(f"First {limit} rows from {table_name}:")
    for r in results:
        print(r)

def main():
    settings = load_settings()
    conn, cur = connect_to_snowflake(settings)
    
    df = pd.read_csv(settings["csv_file"])
    # Snowflake expects uppercase table names
    df.columns = [c.upper() for c in df.columns]
    create_table(cur, settings["table_name"])
    upload_csv(df, conn, settings["table_name"])
    query_table(cur, settings["table_name"])
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
