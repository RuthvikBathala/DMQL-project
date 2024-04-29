# streamlit_app.py

import streamlit as st
import pandas as pd
import psycopg2

# Function to establish PostgreSQL connection
@st.cache(allow_output_mutation=True)
def get_postgres_connection():
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="SupplyChain",
        user="postgres",
        password="pavilion"
    )
    return conn

# Execute query function
def execute_query(query):
    conn = get_postgres_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result

# Main Streamlit app code
st.title("PostgreSQL Database Query Tool")

# User input area
query_type = st.selectbox("Select query type", ["Select", "Update", "Insert", "Delete"])
query = st.text_area("Enter your SQL query here")

# Execute the query based on user input
if st.button("Execute Query"):
    if query_type == "Select":
        results = execute_query(query)
        if results:
            st.write(pd.DataFrame(results))
        else:
            st.write("No results found.")
    else:
        try:
            conn = get_postgres_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            st.write("Query executed successfully.")
        except Exception as e:
            st.error(f"Error executing query: {e}")

