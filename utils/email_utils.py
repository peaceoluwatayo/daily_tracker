import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import urllib.parse
import os
from sib_api_v3_sdk import Configuration, ApiClient, TransactionalEmailsApi, SendSmtpEmail
from database import get_connection
import streamlit as st

# Load environment variables
from dotenv import load_dotenv

load_dotenv()
BREVO_API_KEY = os.getenv("BREVO_API_KEY")
SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL")
BASE_URL = "http://localhost:8501"

def send_confirmation_email(user_email, username, token):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = BREVO_API_KEY
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    verify_link = f"{BASE_URL}?verify={urllib.parse.quote(token)}"
    subject = "Confirm Your Daily Journal Tracker Account"
    html_content = f"""
    <html>
        <body>
            <h2>Hello {username},</h2>
            <p>Thanks for signing up for <b>Daily Journal Tracker</b> 🎉</p>
            <p>Click below to confirm your email address:</p>
            <p><a href="{verify_link}">Verify My Account</a></p>
            <p>Cheers,<br>The Daily Tracker Team</p>
        </body>
    </html>
    """
    email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": user_email, "name": username}],
        sender={"name": "Daily Journal", "email": SENDER_EMAIL},
        subject=subject,
        html_content=html_content
    )

    try:
        api_instance.send_transac_email(email)
        st.success("✅ A verification email has been sent. Please check your inbox.")
    except ApiException as e:
        st.error(f"❌ Failed to send email: {e}")

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

