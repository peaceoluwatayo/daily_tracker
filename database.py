import pyodbc
import uuid
import os
import bcrypt
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Fetch database credentials from environment variables
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

# Establish database connection
def get_connection():
    return pyodbc.connect(conn_str)

# Hashing functions
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

# Add user
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

# Authenticate user
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

# Verify user token
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
