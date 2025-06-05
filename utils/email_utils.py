import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import urllib.parse
import os
from sib_api_v3_sdk import Configuration, ApiClient, TransactionalEmailsApi, SendSmtpEmail
from database import get_connection
import streamlit as st
import uuid

# Load environment variables
from dotenv import load_dotenv

load_dotenv()
BREVO_API_KEY = os.getenv("BREVO_API_KEY")
SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL")
# BASE_URL = "https://daily-journal-tracker.onrender.com"

BASE_URL = "http://localhost:8501"


# BREVO_API_KEY = st.secrets["brevo"]["api_key"]
# SENDER_EMAIL = st.secrets["brevo"]["sender_email"]
# BASE_URL = "https://dailyjournaltracker.streamlit.app"  


def send_confirmation_email(user_email, username, new_token):
    new_token = str(uuid.uuid4())  # Generate new token

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Users SET token = ?, token_used = 0 WHERE email = ?",
            (new_token, user_email)
        )
        conn.commit()

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = BREVO_API_KEY
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    verify_link = f"{BASE_URL}?verify={urllib.parse.quote(new_token)}"
    subject = "Confirm Your Daily Journal Tracker Account"
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; background-color: #f5f5f5; font-size: 16px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 8px;">
        <p style="margin-bottom: 20px;">Hello {username},</p>
        <p style="margin-bottom: 15px;">Thanks for signing up for Daily Journal Tracker.</p>
        <p style="margin-bottom: 15px;">Click the button below to confirm your email address:</p>
        <p style="margin-bottom: 30px; text-align: center;">
            <a href="{verify_link}" 
            style="display: inline-block; padding: 10px 20px; background-color: #007BFF; 
                    color: white; text-decoration: none; border-radius: 5px;">
            Verify My Account
            </a>
        </p>
        <p style="margin-top: 40px;">Cheers,<br>The Daily Journal Tracker Team</p>
        </div>
    </body>
    </html>
    """

    email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": user_email, "name": username}],
        sender={"name": "Daily Journal Tracker", "email": SENDER_EMAIL},
        subject=subject,
        html_content=html_content
    )

    try:
        api_instance.send_transac_email(email)
    except ApiException as e:
        st.error(f"❌ Failed to send email: {e}")


def send_password_reset_email(email):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM Users WHERE email = ?", (email,))
            row = cursor.fetchone()
            if row:
                username = row[0]
                new_token = str(uuid.uuid4())
                cursor.execute(
                    "UPDATE Users SET token = ?, token_used = 0 WHERE email = ?",
                    (new_token, email)
                )
                conn.commit()

                reset_link = f"{BASE_URL}?reset={urllib.parse.quote(new_token)}"
                subject = "Reset Your Password - Daily Journal Tracker"
                html_content = f"""
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; background-color: #f5f5f5;">
                    <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 8px; font-size: 16px;">
                    <p style="margin-bottom: 20px;">Hello {username},</p>
                    <p style="margin-bottom: 15px;">We received a request to reset your password.</p>
                    <p style="margin-bottom: 15px;">Click the button below to create a new password:</p>
                    <p style="margin-bottom: 30px; text-align: center;">
                        <a href="{reset_link}" 
                        style="display: inline-block; padding: 10px 20px; background-color: #007BFF; 
                                color: white; text-decoration: none; border-radius: 5px;">
                        Reset My Password
                        </a>
                    </p>
                    <p style="margin-bottom: 15px;">If you didn’t request this, you can safely ignore this email.</p>
                    <p style="margin-top: 40px;">Cheers,<br>The Daily Journal Tracker Team</p>
                    </div>
                </body>
                </html>
                """

                configuration = Configuration()
                configuration.api_key['api-key'] = BREVO_API_KEY
                api_instance = TransactionalEmailsApi(ApiClient(configuration))

                email_content = SendSmtpEmail(
                    to=[{"email": email, "name": username}],
                    sender={"name": "Daily Journal Tracker", "email": SENDER_EMAIL},
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
