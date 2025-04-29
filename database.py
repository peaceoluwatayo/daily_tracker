import pyodbc
import uuid
import os
import bcrypt
from dotenv import load_dotenv
import urllib.parse
from sib_api_v3_sdk.rest import ApiException
from datetime import datetime
import streamlit as st

# Load environment variables
load_dotenv()

# Brevo settings
BREVO_API_KEY = os.getenv("BREVO_API_KEY")
SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL")
BASE_URL = "http://localhost:8501"  # Update this URL after deployment

# Database credentials
DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Database connection string
conn_str = (
    f'DRIVER={{ODBC Driver 18 for SQL Server}};'
    f'SERVER={DB_SERVER};DATABASE={DB_NAME};'
    f'UID={DB_USERNAME};PWD={DB_PASSWORD};'
    f'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
)

def get_connection():
    return pyodbc.connect(conn_str)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def add_user(username, password, email):
    token = uuid.uuid4()
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Users WHERE username = ? OR email = ?", username, email)
            if cursor.fetchone():
                return False, None
            hashed_password = hash_password(password)
            cursor.execute(
                """
                INSERT INTO Users (username, password, email, verified, token)
                VALUES (?, ?, ?, 0, ?)
                """,
                (username, hashed_password.decode('utf-8'), email, token)
            )
            conn.commit()
            return True, str(token)
    except Exception as e:
        print("Error adding user:", e)
        return False, None

def authenticate_user(username, password):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password, verified FROM Users WHERE username = ?", username)
            row = cursor.fetchone()
            if not row:
                return "invalid"
            db_password, verified = row
            if not check_password(password, db_password.encode('utf-8')):
                return "invalid"
            if not verified:
                return "unverified"
            return "success"
    except Exception as e:
        print("Authentication error:", e)
        return "invalid"

def verify_user_token(token):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM Users WHERE token = ?", token)
            row = cursor.fetchone()
            if row:
                cursor.execute("UPDATE Users SET verified = 1 WHERE token = ?", token)
                conn.commit()
                return True
            return False
    except Exception as e:
        print("Token verification error:", e)
        return False

def reset_password(token, new_password):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM Users WHERE token = ?", token)
            row = cursor.fetchone()
            if row:
                hashed_password = hash_password(new_password)
                cursor.execute(
                    "UPDATE Users SET password = ? WHERE token = ?",
                    (hashed_password.decode('utf-8'), token)
                )
                conn.commit()
                return True
            return False
    except Exception as e:
        print("Reset password error:", e)
        return False

# Function to check if the user has filled the form for today
def has_filled_form_today(username):
    conn = get_connection()
    cursor = conn.cursor()
    
    today = datetime.now().date()  # Get today's date (without time)
    query = """
        SELECT COUNT(*) FROM DailyEntries
        WHERE username = ? AND CAST(entry_date AS DATE) = ?
    """
    cursor.execute(query, (username, today))
    result = cursor.fetchone()
    conn.close()
    
    return result[0] > 0 

# Function to save entry to the database
def save_entry_to_db(entry):
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO DailyEntries (
                username,
                entry_date, mood, food, water_intake, exercise, social,
                sleep_quality, sleep_time, sleep_duration
            )
            OUTPUT INSERTED.entry_id
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            entry["username"], 
            datetime.now(),
            entry["mood"], 
            entry["food"],  
            entry["water"], 
            entry["exercise"], 
            entry["social"], 
            entry["sleep_quality"], 
            entry["sleep_time"], 
            entry["sleep_duration"]
        ))
        
        entry_id = cursor.fetchone()[0]  # Capture the newly inserted entry_id
        conn.commit()
        conn.close()
        return entry_id
    
    except Exception as e:
        st.error(f"Failed to save entry: {str(e)}")
        return None

 # Function to save scores to the database   
def save_scores_to_db(scores):
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO DailyScores (
                entry_id, username, entry_date,
                mood_score, food_score, water_score, exercise_score, social_score,
                sleep_quality_score, sleep_time_score, sleep_duration_score
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            scores["entry_id"],
            scores["username"],
            datetime.now(),
            scores["mood_score"],
            scores["food_score"],
            scores["water_score"],
            scores["exercise_score"],
            scores["social_score"],
            scores["sleep_quality_score"],
            scores["sleep_time_score"],
            scores["sleep_duration_score"]
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"Failed to save scores: {str(e)}")
