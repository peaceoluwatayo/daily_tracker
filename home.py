import streamlit as st
from pages import show_signup, show_forgot_password, show_login
from pages import handle_verification, handle_reset_token, show_dashboard, show_tracker_form, show_history, show_home_page

# Set page config to disable sidebar and use full-width layout
st.set_page_config(page_title="Daily Journal Tracker", layout="wide", initial_sidebar_state="collapsed")


def main():
    if "page" not in st.session_state:
        st.session_state.page = "login"
    
    # Handle verification and password reset token from URL query params
    if "verify" in st.query_params:
        handle_verification()
    elif "reset" in st.query_params:
        handle_reset_token()

    # Page navigation based on session state
    if st.session_state.page == "login":
        show_login()
    elif st.session_state.page == "signup":
        show_signup()
    elif st.session_state.page == "forgot_password":
        show_forgot_password()
    elif st.session_state.page == "first":
        show_home_page()
    elif st.session_state.page == "dashboard":
        show_dashboard()
    elif st.session_state.page == "tracker_form":
        show_tracker_form()
    elif st.session_state.page == "history":
        show_history()
    
if __name__ == "__main__":
    main()


