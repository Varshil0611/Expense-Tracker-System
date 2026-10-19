import hashlib
import streamlit as st
import database

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return True
    return False

def create_user(username, password, name):
    conn = database.create_connection()
    if not conn:
        return False
    
    hashed_password = make_hashes(password)
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, name) VALUES (%s, %s, %s)", 
                       (username, hashed_password, name))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error creating user: {e}")
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = database.create_connection()
    if not conn:
        return None
    
    hashed_password = make_hashes(password)
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", 
                       (username, hashed_password))
        user = cursor.fetchone()
        return user
    except Exception as e:
        st.error(f"Error logging in: {e}")
        return None
    finally:
        conn.close()
