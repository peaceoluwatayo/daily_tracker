import streamlit as st
from database import add_user, authenticate_user, verify_user_token
from dotenv import load_dotenv
import os
import urllib.parse

# Brevo email libraries
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

# Load .env variables
load_dotenv()
BREVO_API_KEY = os.getenv("BREVO_API_KEY")
SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL")

# Base URL for verification link (adjust if deployed)
BASE_URL = "http://localhost:8501"  # Update to actual URL after deployment

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "login"

# Send verification email using Brevo
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
        <p>Please confirm your email address by clicking the link below:</p>
        <p><a href="{verify_link}">Verify My Account</a></p>
        <br>
        <p>Cheers,<br>The Daily Tracker Team</p>
      </body>
    </html>
    """

    sender = {"name": "Daily Journal", "email": SENDER_EMAIL}
    to = [{"email": user_email, "name": username}]

    email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        sender=sender,
        subject=subject,
        html_content=html_content
    )

    try:
        api_instance.send_transac_email(email)
        st.success("✅ A verification email has been sent. Please check your inbox.")
    except ApiException as e:
        st.error(f"❌ Failed to send email: {e}")

# Login Page
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
                # Show main app/dashboard here
            else:
                st.error("❌ Invalid username or password.")
        else:
            st.warning("Please enter both username and password.")

    # Display message and button on the same line with balanced space
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("<p style='margin-bottom: 0;'>Don't have an account?</p>", unsafe_allow_html=True)
    with col2:
        if st.button("Sign Up"):
            st.session_state.page = "signup"
            st.rerun()

# Signup Page
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
                st.warning("⚠️ Username already exists. Please choose another.")
        else:
            st.warning("Please fill in all fields.")

    # Display message and button on the same line with balanced space
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("<p style='margin-bottom: 0;'>Already have an account?</p>", unsafe_allow_html=True)
    with col2:
        if st.button("Login"):
            st.session_state.page = "login"
            st.rerun()

# Email verification handler
def handle_verification():
    query_params = st.query_params
    token = query_params.get("verify")

    if token:
        verified = verify_user_token(token)
        if verified:
            st.success("✅ Your account has been verified! You can now login.")
        else:
            st.error("❌ Invalid or expired verification link.")
        st.session_state.page = "login"

# Main App Logic
def main():
    handle_verification()

    if st.session_state.page == "login":
        show_login()
    elif st.session_state.page == "signup":
        show_signup()

if __name__ == '__main__':
    main()
