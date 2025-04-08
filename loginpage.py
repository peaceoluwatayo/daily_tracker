import streamlit as st
from database import add_user, authenticate_user
from dotenv import load_dotenv
import os

# Brevo email libraries
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

# Load .env variables
load_dotenv()
BREVO_API_KEY = os.getenv("BREVO_API_KEY")
SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL")

# Initialize session state to track current page
if "page" not in st.session_state:
    st.session_state.page = "login"  # Default page is login

# Function to send confirmation email using Brevo
def send_confirmation_email(user_email, username):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = BREVO_API_KEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    subject = "Welcome to Daily Journal Tracker!"
    html_content = f"""
    <html>
      <body>
        <h2>Hello {username},</h2>
        <p>Thanks for signing up with <b>Daily Journal Tracker</b> 🎉</p>
        <p>You can now start tracking your goals and progress daily.</p>
        <br>
        <p>Cheers, <br> The Daily Tracker Team</p>
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
        response = api_instance.send_transac_email(email)
        st.success("✅ Confirmation email sent successfully!")
    except ApiException as e:
        st.error(f"❌ Failed to send email: {e}")

# Login Page
def show_login():
    st.title("📘 Daily Journal Tracker")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            if authenticate_user(username, password):
                st.success(f"Welcome back, {username}! 👋")
                # Proceed to user dashboard here
            else:
                st.error("❌ Invalid username or password.")
        else:
            st.warning("Please enter both username and password.")

    if st.button("Don't have an account? Sign Up"):
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
            success = add_user(new_user, new_pass)
            if success:
                send_confirmation_email(email, new_user)
                st.success("✅ Account created successfully! You can now login.")
                st.session_state.page = "login"
                st.rerun()
            else:
                st.warning("⚠️ Username already exists. Please choose another.")
        else:
            st.warning("Please enter all required fields.")

    if st.button("Already have an account? Login"):
        st.session_state.page = "login"
        st.rerun()

# Main App Logic
def main():
    if st.session_state.page == "login":
        show_login()
    elif st.session_state.page == "signup":
        show_signup()

if __name__ == '__main__':
    main()
