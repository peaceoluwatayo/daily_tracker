# import streamlit as st
# from database import verify_user_token
# from utils.email_utils import send_password_reset_email
# from pages import show_reset_password


# def show_forgot_password():
#     st.title("🔐 Reset Your Password")
#     email = st.text_input("Enter your email address")

#     if st.button("Send Reset Link"):
#         if email:
#             success = send_password_reset_email(email)
#             if success:
#                 st.success("✅ A password reset link has been sent to your email.")
#             else:
#                 st.error("❌ Email not found or error sending email.")
#         else:
#             st.warning("Please enter your email address.")

#     if st.button("Back to Login"):
#         st.session_state.page = "login"
#         st.rerun()

# def handle_verification():
#     query_params = st.query_params
#     token = query_params.get("verify")
#     if token:
#         verified = verify_user_token(token)
#         if verified:
#             st.success("✅ Your account has been verified! You can now login.")
#         else:
#             st.error("❌ Invalid or expired verification link.")
#         st.stop()

# def handle_reset_token():
#     query_params = st.query_params
#     token = query_params.get("reset")
#     if token:
#         show_reset_password(token)
#         st.stop()


import streamlit as st
from database import verify_user_token
from utils.email_utils import send_password_reset_email
from pages import show_reset_password


def show_forgot_password():
    # st.set_page_config(page_title="Forgot Password", layout="centered")

    # Add vertical space to center form
    for _ in range(6):
        st.empty()

    # Center horizontally with columns
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            st.markdown(
                """
                <div style="text-align: center;">
                    <h2>🔐 Reset Your Password</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

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

    # Add bottom vertical spacing
    for _ in range(4):
        st.empty()


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


