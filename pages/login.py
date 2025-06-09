import streamlit as st
import random
import string
from captcha.image import ImageCaptcha
from io import BytesIO
from database import authenticate_user

def generate_captcha_text(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def show_login():
    for _ in range(6):
        st.empty()

    if 'captcha_text' not in st.session_state or st.session_state.get('refresh_captcha', True):
        st.session_state.captcha_text = generate_captcha_text()
        st.session_state.refresh_captcha = False

    image = ImageCaptcha(width=280, height=90)
    captcha_text = st.session_state.captcha_text
    buffer = BytesIO()
    captcha_image = image.generate_image(captcha_text)
    captcha_image.save(buffer, format="PNG")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            st.markdown("<div style='text-align: center;'><h2>📘 Daily Journal Tracker</h2></div>", unsafe_allow_html=True)

            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")

                st.image(buffer.getvalue(), caption="Enter the CAPTCHA text above")
                captcha_input = st.text_input("Enter CAPTCHA")

                submitted = st.form_submit_button("Login")

                if submitted:
                    if username and password and captcha_input:
                        if captcha_input.strip() != st.session_state.captcha_text:
                            st.error("❌ CAPTCHA did not match. Please try again.")
                            st.session_state.refresh_captcha = False
                        else:
                            result = authenticate_user(username, password)
                            if result == "unverified":
                                st.warning("⚠️ Please verify your email before logging in.")
                            elif result == "success":
                                st.session_state.logged_in = True
                                st.session_state.username = username
                                st.session_state.page = "dashboard"
                                st.rerun()
                            else:
                                st.error("❌ Invalid username or password.")
                    else:
                        st.warning("Please enter both username and password, and solve the CAPTCHA.")

            # Buttons outside form
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Sign Up"):
                    st.session_state.page = "signup"
                    st.rerun()
            with col_b:
                if st.button("Forgot Password?"):
                    st.session_state.page = "forgot_password"
                    st.rerun()

    for _ in range(4):
        st.empty()
