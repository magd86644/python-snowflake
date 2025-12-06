import streamlit as st
import pandas as pd
from snowflake_utils import load_settings, connect_to_snowflake, query_table, create_table

# --- Connect to Snowflake ---
settings = load_settings()
conn, cur = connect_to_snowflake(settings)

st.title("Snowflake Query Tester & AI Tools")

# --- Table structure info ---
st.subheader(f"Table Structure: {settings['table_name']}")
st.markdown("""
| Column Name | Data Type |
|-------------|-----------|
| patient_id  | INT       |
| first_name  | STRING    |
| last_name   | STRING    |
| birth_date  | DATE      |
| gender      | STRING    |
| diagnosis   | STRING    |
| visit_date  | DATE      |
| treatment   | STRING    |
| cost        | FLOAT     |
""")

# --- Table creation ---
st.subheader("Create Table")
if st.button(f"Create table '{settings['table_name']}'"):
    try:
        create_table(cur, settings["table_name"])
        st.success(f"Table '{settings['table_name']}' created (if not exists).")
    except Exception as e:
        st.error(f"Error creating table: {e}")

# --- Regular SQL query section ---
st.subheader("Run SQL Query")
user_query = st.text_area("Enter your SQL query:")
if st.button("Run SQL Query"):
    if user_query.strip() != "":
        try:
            results = query_table(cur, user_query)
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df)
            else:
                st.write("Query ran successfully, no results to display.")
        except Exception as e:
            st.error(f"Error: {e}")

# --- AI query section ---
st.subheader("Run Snowflake AI Query")
st.markdown("You can ask Snowflake to summarize patient treatments or predict values using AI functions.")
ai_prompt = st.text_area("Enter AI task (e.g., summarize treatments or suggest insights):")
if st.button("Run AI Query"):
    if ai_prompt.strip() != "":
        try:
            # Example using SYSTEM$AI_SUMMARIZE (for text summarization)
            ai_query = f"""
            SELECT SYSTEM$AI_SUMMARIZE(
                ARRAY_AGG(DIAGNOSIS || ' - ' || TREATMENT),
                '{ai_prompt}'
            ) AS ai_result
            FROM {settings['table_name']};
            """
            results = query_table(cur, ai_query)
            if results:
                st.write("AI Result:")
                st.write(results[0][0])
            else:
                st.write("AI query ran successfully, no results.")
        except Exception as e:
            st.error(f"Error: {e}")

# --- Close connection ---
st.button("Close Connection", on_click=lambda: (cur.close(), conn.close()))
