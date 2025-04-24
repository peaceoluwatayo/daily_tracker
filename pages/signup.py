import streamlit as st
from database import add_user
from utils.email_utils import send_confirmation_email

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
