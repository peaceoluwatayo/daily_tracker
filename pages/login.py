import streamlit as st
from database import authenticate_user


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
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.page = "first"
                st.rerun()
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
