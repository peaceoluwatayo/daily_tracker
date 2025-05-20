import streamlit as st
import pyodbc
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# # Load environment variables
# load_dotenv()

# # Database credentials
# DB_SERVER = os.getenv("DB_SERVER")
# DB_NAME = os.getenv("DB_NAME")
# DB_USERNAME = os.getenv("DB_USERNAME")
# DB_PASSWORD = os.getenv("DB_PASSWORD")


# Database credentials
DB_SERVER = st.secrets["azure_db"]["server"]
DB_NAME = st.secrets["azure_db"]["name"]
DB_USERNAME = st.secrets["azure_db"]["username"]
DB_PASSWORD = st.secrets["azure_db"]["password"]

# Database connection string
conn_str = (
    f'DRIVER={{ODBC Driver 18 for SQL Server}};'
    f'SERVER={DB_SERVER};DATABASE={DB_NAME};'
    f'UID={DB_USERNAME};PWD={DB_PASSWORD};'
    f'Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=30;'
)

def show_history():
    st.markdown("<h1 style='text-align: center;'>📜 History</h1>", unsafe_allow_html=True)

    # Place Back to Home on the left and Logout on the right
    col1, col2 = st.columns([8, 1])
    with col1:
        if st.button("Back to Home"):
            st.session_state.page = "first"  # or "home" depending on your naming
            st.rerun()
    with col2:
        if st.button("Logout"):
            st.session_state.clear()
            st.session_state.page = "login"
            st.rerun()

    # Check for logged-in user
    username = st.session_state.get("username")
    if not username:
        st.warning("You must be logged in to view your history.")
        return

    # Date Range Filter - user selects the number of days
    date_range = st.selectbox(
        "Select Date Range:",
        ["Last 7 Days", "Last 14 Days", "Last 30 Days", "All Time"],
        index=0  # Set default to "Last 7 Days"
    )

    # Determine the start date based on the selected range
    today = datetime.now()
    if date_range == "Last 7 Days":
        start_date = today - timedelta(days=7)
    elif date_range == "Last 14 Days":
        start_date = today - timedelta(days=14)
    elif date_range == "Last 30 Days":
        start_date = today - timedelta(days=30)
    else:
        start_date = None  # "All Time"

    # SQL Query to fetch history based on the selected date range
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        if start_date:
            cursor.execute("""
                SELECT 
                    entry_date, mood, food, water_intake, exercise, 
                    social, sleep_quality, sleep_time, sleep_duration
                FROM DailyEntries
                WHERE username = ? AND entry_date >= ?
                ORDER BY entry_date DESC
            """, (username, start_date))
        else:
            cursor.execute("""
                SELECT 
                    entry_date, mood, food, water_intake, exercise, 
                    social, sleep_quality, sleep_time, sleep_duration
                FROM DailyEntries
                WHERE username = ?
                ORDER BY entry_date DESC
            """, (username,))

        rows = cursor.fetchall()

        if not rows:
            st.info("No entries found for the selected date range.")
            return

        # Convert the fetched rows into a DataFrame for easier manipulation
        df = pd.DataFrame.from_records(
            rows,
            columns=[
                "Date", "Mood", "Food", "Water Intake", "Exercise",
                "Social", "Sleep Quality", "Sleep Time", "Sleep Duration"
            ]
        )

        # Format the Date column to a readable format
        df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d %H:%M")

        # Create a custom HTML table to avoid word wrapping and add index numbers
        table_html = """
        <style>
            td, th {
                white-space: nowrap; 
                padding: 8px 12px;
                border: 1px solid #ddd;
            }
            table {
                width: 100%;
                border-collapse: collapse;
            }
            .table-container {
                overflow-x: auto; /* Horizontal scrollbar */
                -webkit-overflow-scrolling: touch;
                margin-top: 20px;
                border: 1px solid #ddd;
            }
        </style>
        <div class="table-container">
        <table>
        <tr>
            <th>No.</th>  <!-- Row number -->
        """

        # Add table headers, including a header for the row number
        for col in df.columns:
            table_html += f"<th>{col}</th>"
        table_html += "</tr>"

        # Add table rows with index number
        for idx, row in df.iterrows():
            table_html += "<tr>"
            table_html += f"<td>{idx + 1}</td>"  # Add the row number (index + 1 to start from 1)

            # Add the rest of the columns
            for item in row:
                table_html += f"<td>{item}</td>"
            table_html += "</tr>"

        table_html += "</table></div>"

        st.markdown(table_html, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error fetching history: {str(e)}")
