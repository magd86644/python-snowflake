import pandas as pd
import snowflake.connector
from dotenv import load_dotenv
import os

load_dotenv()  

user = os.getenv("SNOWFLAKE_USER")
password = os.getenv("SNOWFLAKE_PASSWORD")
account = os.getenv("SNOWFLAKE_ACCOUNT")
warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
database = os.getenv("SNOWFLAKE_DATABASE")
schema = os.getenv("SNOWFLAKE_SCHEMA")


conn = snowflake.connector.connect(
    user=user,
    password=password,
    account=account,
    warehouse=warehouse,
    database=database,
    schema=schema
)
cur = conn.cursor()

cur.execute("SELECT CURRENT_VERSION();")
print(cur.fetchall())

cur.close()
conn.close()
