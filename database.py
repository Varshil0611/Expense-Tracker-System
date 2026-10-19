import mysql.connector
import streamlit as st

def create_connection():
    """
    Establishes a connection to the MySQL database.
    Attempts to connect using default local credentials or Streamlit secrets.
    """
    try:
        # Try connecting with default credentials (commonly used in local dev)
        # You might need to adjust 'user' and 'password' based on your local setup
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        
        # Create database if it doesn't exist
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS expense_tracker_db")
        
        # Connect to the specific database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="expense_tracker_db"
        )
        return mydb
    except mysql.connector.Error as err:
        st.error(f"Error connecting to database: {err}")
        return None

def run_query(query, params=None):
    """
    Executes a SQL query and returns the result (for SELECT) 
    or commits changes (for INSERT/UPDATE/DELETE).
    """
    conn = create_connection()
    if conn is None:
        return None
    
    try:
        cursor = conn.cursor(dictionary=True)
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
        if query.strip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
            conn.commit()
            return cursor.lastrowid
        else:
            return cursor.fetchall()
            
    except mysql.connector.Error as err:
        st.error(f"Query Error: {err}")
        return None
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
