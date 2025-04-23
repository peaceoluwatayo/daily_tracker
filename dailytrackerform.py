import streamlit as st
import pyodbc
import os
from datetime import datetime

# Database credentials from environment variables
DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# ODBC connection string
conn_str = (
    f'DRIVER={{ODBC Driver 18 for SQL Server}};'
    f'SERVER={DB_SERVER};DATABASE={DB_NAME};'
    f'UID={DB_USERNAME};PWD={DB_PASSWORD};'
    f'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
)

# Function to check if an entry already exists for today
def check_entry_exists():
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM DailyEntries 
            WHERE CAST(entry_date AS DATE) = CAST(GETDATE() AS DATE)
        """)
        result = cursor.fetchone()
        conn.close()
        return result[0] > 0
    except Exception as e:
        return False

# Function to save entry to the database
def save_entry_to_db(entry):
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO DailyEntries (
                entry_date, mood, breakfast, lunch, dinner, water_intake, exercise, 
                family_social, friend_social, neighbour_social, stranger_social, 
                sleep_quality, sleep_time, sleep_duration
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now(),
            entry["mood"],
            entry["breakfast"],
            entry["lunch"],
            entry["dinner"],
            entry["water"],
            entry["exercise"],
            entry["family_social"],
            entry["friend_social"],
            entry["neighbour_social"],
            entry["stranger_social"],
            entry["sleep_quality"],
            entry["sleep_time"],
            entry["sleep_duration"]
        ))
        conn.commit()
        conn.close()
        return True, "Entry saved successfully!"
    except Exception as e:
        return False, f"Failed to save entry: {str(e)}"

# Streamlit UI
st.title("📝 Daily Journal Tracker")

mood = st.selectbox("1. How are you feeling today?", [
    "Excited", "Happy", "Contented", "Low", "Depressed"
])

breakfast = st.selectbox("2. What did you eat for breakfast today?", [
    "Healthy balanced", "Easy food/Snacks"
])

lunch = st.selectbox("3. What did you eat for lunch today?", [
    "Healthy balanced", "Easy food/Snacks"
])

dinner = st.selectbox("4. What did you eat for dinner today?", [
    "Healthy balanced", "Easy food/Snacks"
])

water = st.selectbox("5. How was your water intake today?", [
    "Adequate (>1 litre)", "Low (<1 litre)"
])

exercise = st.selectbox("6. Did you exercise today?", [
    "Gym", "Cycle", "Run", "Walk", "I didn't exercise today"
])

family_social = st.selectbox("7. How did you socialize with family today?", [
    "In person", "By Phone", "By Text/Message"
])

friend_social = st.selectbox("8. How did you socialize with friends today?", [
    "In person", "By Phone", "By Text/Message"
])

neighbour_social = st.selectbox("9. How did you socialize with neighbours today?", [
    "In person", "By Phone", "By Text/Message"
])

stranger_social = st.selectbox("10. How did you socialize with strangers today?", [
    "In person", "By Phone", "By Text/Message"
])

sleep_quality = st.selectbox("11. How was your sleep last night?", [
    "Excellent", "Good", "Average", "Poor", "Very poor"
])

sleep_time = st.selectbox("12. What time did you go to bed last night?", [
    "9pm", "10pm", "11pm", "Midnight", "After Midnight"
])

sleep_duration = st.selectbox("13. How many hours of sleep did you get last night?", [
    "Less than 3 hours", "3-4 hours", "5-6 hours", "7-8 hours", "8+ hours"
])

if check_entry_exists():
    st.warning("You have already submitted your entry for today!")
else:
    if st.button("Submit Entry"):
        entry = {
            "mood": mood,
            "breakfast": breakfast,
            "lunch": lunch,
            "dinner": dinner,
            "water": water,
            "exercise": exercise,
            "family_social": family_social,
            "friend_social": friend_social,
            "neighbour_social": neighbour_social,
            "stranger_social": stranger_social,
            "sleep_quality": sleep_quality,
            "sleep_time": sleep_time,
            "sleep_duration": sleep_duration
        }

        success, message = save_entry_to_db(entry)
        if success:
            st.success(message)
        else:
            st.error(message)
