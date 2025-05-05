# import streamlit as st
# from database import authenticate_user


# def show_login():
#     st.title("📘 Daily Journal Tracker")

#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")

#     if st.button("Login"):
#         if username and password:
#             result = authenticate_user(username, password)
#             if result == "unverified":
#                 st.warning("⚠️ Please verify your email before logging in.")
#             elif result == "success":
#                 st.session_state.logged_in = True
#                 st.session_state.username = username
#                 st.session_state.page = "first"
#                 st.rerun()
#             else:
#                 st.error("❌ Invalid username or password.")
#         else:
#             st.warning("Please enter both username and password.")

#     col1, col2 = st.columns([1, 1])
#     with col1:
#         if st.button("Sign Up"):
#             st.session_state.page = "signup"
#             st.rerun()
#     with col2:
#         if st.button("Forgot Password?"):
#             st.session_state.page = "forgot_password"
#             st.rerun()


import streamlit as st
from database import authenticate_user

def show_login():
    # st.set_page_config(page_title="Login", layout="centered")

    # Add vertical spacing to center the content
    for _ in range(6):
        st.empty()

    # Create centered column layout
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            st.markdown(
                """
                <div style="text-align: center;">
                    <h2>📘 Daily Journal Tracker</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

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

            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Sign Up"):
                    st.session_state.page = "signup"
                    st.rerun()
            with col_b:
                if st.button("Forgot Password?"):
                    st.session_state.page = "forgot_password"
                    st.rerun()

    # Add vertical spacing after the form
    for _ in range(4):
        st.empty()
