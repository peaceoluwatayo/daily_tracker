import streamlit as st
from database import (
    add_user, authenticate_user, verify_user_token,
    send_password_reset_email, reset_password
)
from dotenv import load_dotenv
import os
import urllib.parse
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

# Load env variables
load_dotenv()
BREVO_API_KEY = os.getenv("BREVO_API_KEY")
SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL")
BASE_URL = "http://localhost:8501"

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "login"

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

def show_login():
    st.title("📘 Daily Journal Tracker")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            result = authenticate_user(username, password)
            if result == "unverified":
                st.warning("⚠️ Please verify your email before logging in.")
            elif result == "success":
                st.success(f"Welcome back, {username}! 👋")
            else:
                st.error("❌ Invalid username or password.")
        else:
            st.warning("Please enter both username and password.")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Sign Up"):
            st.session_state.page = "signup"
            st.rerun()
    with col2:
        if st.button("Forgot Password?"):
            st.session_state.page = "forgot_password"
            st.rerun()

def show_signup():
    st.title("🆕 Create New Account")

    new_user = st.text_input("Choose a username")
    new_pass = st.text_input("Choose a password", type="password")
    email = st.text_input("Enter your email address")

    if st.button("Sign Up"):
        if new_user and new_pass and email:
            success, token = add_user(new_user, new_pass, email)
            if success:
                send_confirmation_email(email, new_user, token)
            else:
                st.warning("⚠️ Username or email already exists.")
        else:
            st.warning("Please fill in all fields.")

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()

def show_forgot_password():
    st.title("🔐 Reset Your Password")
    email = st.text_input("Enter your email address")

    if st.button("Send Reset Link"):
        if email:
            success = send_password_reset_email(email)
            if success:
                st.success("✅ A password reset link has been sent to your email.")
            else:
                st.error("❌ Email not found or error sending email.")
        else:
            st.warning("Please enter your email address.")

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()

def show_reset_password(token):
    st.title("🔑 Set New Password")

    new_password = st.text_input("Enter New Password", type="password")

    if st.button("Reset Password"):
        if new_password:
            success = reset_password(token, new_password)
            if success:
                st.success("✅ Your password has been successfully reset.")
                st.info("You can now log in with your new password.")
            else:
                st.error("❌ Invalid or expired reset link.")
        else:
            st.warning("Please enter a new password.")

def handle_verification():
    query_params = st.query_params
    token = query_params.get("verify")
    if token:
        verified = verify_user_token(token)
        if verified:
            st.success("✅ Your account has been verified! You can now login.")
        else:
            st.error("❌ Invalid or expired verification link.")
        st.stop()

def handle_reset_token():
    query_params = st.query_params
    token = query_params.get("reset")
    if token:
        show_reset_password(token)
        st.stop()

def main():
    handle_verification()
    handle_reset_token()

    if st.session_state.page == "login":
        show_login()
    elif st.session_state.page == "signup":
        show_signup()
    elif st.session_state.page == "forgot_password":
        show_forgot_password()

if __name__ == "__main__":
    main()
