import streamlit as st
import mysql.connector
import pandas as pd
st.set_page_config(page_title="MySQL Streamlit App", layout="wide")
st.title("🗄️ MySQL Database Explorer")
host = "localhost"
user = "root"
password = "jatin"
database = "sunbeam"
@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        autocommit=True
    )
try:
    connection = get_connection()
    st.success("Connected to MySQL database")
    st.subheader("Tables in Database")
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    cursor.close()
    table_list = [table[0] for table in tables]
    selected_table = st.selectbox("Select a table to preview", table_list)
    if selected_table:
        query = f"SELECT * FROM {selected_table} LIMIT 5"
        df = pd.read_sql(query, connection)
        st.subheader(f"Preview of `{selected_table}`")
        st.dataframe(df)
    st.subheader("Run Your Own SELECT Query")
    user_query = st.text_area(
        "Enter SQL query (SELECT only)",
        placeholder="SELECT * FROM employees WHERE salary > 50000;"
    )
    if st.button("Run Query"):
        if user_query.strip().lower().startswith("select"):
            try:
                result_df = pd.read_sql(user_query, connection)
                st.success("Query executed successfully")
                st.dataframe(result_df)
            except Exception as e:
                st.error(f"Query Error: {e}")
        else:
            st.error("Only SELECT queries are allowed")
except mysql.connector.Error as error:
    st.error(f"Database Error: {error}")
