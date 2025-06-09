import streamlit as st
from database import verify_user_token
from utils.email_utils import send_password_reset_email
from pages import show_reset_password
import random
import string
from captcha.image import ImageCaptcha
from io import BytesIO

# Generate random CAPTCHA text
def generate_captcha_text(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def show_forgot_password():
    # If reset link was sent previously, show only success message
    if st.session_state.get("reset_link_sent", False):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.success("✅ A password reset link has been sent to your email.")
            if st.button("Back to Login"):
                st.session_state.page = "login"
                st.session_state.reset_link_sent = False
                st.rerun()
    
        return  # Exit early to prevent rendering the form again
    

    # Add vertical space to center form
    for _ in range(6):
        st.empty()

    if 'captcha_text' not in st.session_state or st.session_state.get('refresh_captcha', True):
        st.session_state.captcha_text = generate_captcha_text()
        st.session_state.refresh_captcha = False

    # Generate CAPTCHA image in memory
    image = ImageCaptcha(width=280, height=90)
    captcha_text = st.session_state.captcha_text
    captcha_image = image.generate_image(captcha_text)
    buffer = BytesIO()
    captcha_image.save(buffer, format="PNG")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            st.markdown(
                "<div style='text-align: center;'><h2>🔐 Reset Your Password</h2></div>",
                unsafe_allow_html=True,
            )

            with st.form("forgot_password_form"):
                email = st.text_input("Enter your email address")

                # CAPTCHA
                st.image(buffer.getvalue(), caption="Enter the CAPTCHA text above")
                captcha_input = st.text_input("Enter CAPTCHA")

                submitted = st.form_submit_button("Send Reset Link")

                if submitted:
                    if email and captcha_input:
                        if captcha_input.strip() != st.session_state.captcha_text:
                            st.warning("❌ CAPTCHA did not match. Please try again.")
                            st.session_state.refresh_captcha = False
                        else:
                            success = send_password_reset_email(email)
                            if success:
                                st.session_state.reset_link_sent = True
                                st.rerun()
                            else:
                                st.error("❌ Email not found or error sending email.")
                    else:
                        st.warning("Please enter your email address and CAPTCHA.")

            if st.button("Back to Login"):
                st.session_state.page = "login"
                st.rerun()

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
