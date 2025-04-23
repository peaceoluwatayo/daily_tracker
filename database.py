import pyodbc
import uuid
import os
import bcrypt
from dotenv import load_dotenv
import urllib.parse
from sib_api_v3_sdk import Configuration, ApiClient, TransactionalEmailsApi, SendSmtpEmail
from sib_api_v3_sdk.rest import ApiException

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

def send_password_reset_email(email):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username, token FROM Users WHERE email = ?", email)
            row = cursor.fetchone()
            if row:
                username, token = row
                reset_link = f"{BASE_URL}?reset={urllib.parse.quote(token)}"
                subject = "Reset Your Password - Daily Journal Tracker"
                html_content = f"""
                <html>
                    <body>
                        <h2>Hello {username},</h2>
                        <p>We received a request to reset your password.</p>
                        <p>Click the link below to create a new password:</p>
                        <p><a href="{reset_link}">Reset My Password</a></p>
                        <br>
                        <p>If you didn’t request this, you can safely ignore this email.</p>
                        <p>Cheers,<br>The Daily Tracker Team</p>
                    </body>
                </html>
                """

                configuration = Configuration()
                configuration.api_key['api-key'] = BREVO_API_KEY
                api_instance = TransactionalEmailsApi(ApiClient(configuration))

                email_content = SendSmtpEmail(
                    to=[{"email": email, "name": username}],
                    sender={"name": "Daily Journal", "email": SENDER_EMAIL},
                    subject=subject,
                    html_content=html_content
                )

                api_instance.send_transac_email(email_content)
                return True
            return False
    except ApiException as e:
        print("Brevo API error:", e)
        return False
    except Exception as e:
        print("Password reset error:", e)
        return False
