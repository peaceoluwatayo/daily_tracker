import streamlit as st

def show_dashboard():
    st.title("📊 Dashboard")

    # Place Back to Home on the left and Logout on the right
    col1, col2 = st.columns([8, 1])
    with col1:
        if st.button("Back to Home"):
            st.session_state.page = "first"  # or "home" depending on your naming
            st.rerun()
    with col2:
        if st.button("Logout"):
            st.session_state.clear()
            st.session_state.page = "login"
            st.rerun()

    # Add dashboard content here, like summary visualizations, etc.
    st.write("Welcome to your dashboard!")
