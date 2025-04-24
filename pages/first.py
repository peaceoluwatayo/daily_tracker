import streamlit as st

def show_home_page():

    col1, col2 = st.columns([8, 1])
    with col2:
        if st.button("Logout"):
            st.session_state.clear()
            st.session_state.page = "login"
            st.rerun()

    if st.session_state.get("logged_in", False):
        st.success(f"Welcome, {st.session_state['username']}! 👋")
        st.session_state.logged_in = False

    st.title("What would you like to do today?")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📋 Fill Daily Tracker Form"):
            st.session_state.page = "tracker_form"
            st.rerun()

    with col2:
        if st.button("📊 View Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()

    with col3:
        if st.button("📜 View History"):
            st.session_state.page = "history"
            st.rerun()
