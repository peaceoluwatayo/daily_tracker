import streamlit as st
import re
from database import reset_password
from captcha.image import ImageCaptcha
from io import BytesIO
import random
import string

# Generate random CAPTCHA text
def generate_captcha_text(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def show_reset_password(token):
    # Add vertical spacing
    for _ in range(6):
        st.empty()

    if 'captcha_text' not in st.session_state or st.session_state.get('refresh_captcha', True):
        st.session_state.captcha_text = generate_captcha_text()
        st.session_state.refresh_captcha = False

    # Check if password reset was successful before showing form
    if st.session_state.get("password_reset_success"):
        st.success("✅ Your password has been successfully reset.")
        return  
    
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
                "<div style='text-align: center;'><h2>🔑 Set New Password</h2></div>",
                unsafe_allow_html=True,
            )

            with st.form("reset_password_form"):
                new_password = st.text_input("Enter New Password", type="password")

                # Password instruction below input
                st.markdown(
                    '<p style="font-size: medium; color: gray;">Password must be at least 8 characters with a capital letter, lowercase letter, number, special character, and no spaces.</p>',
                    unsafe_allow_html=True,
                )

                st.image(buffer.getvalue(), caption="Enter the CAPTCHA text above")
                captcha_input = st.text_input("Enter CAPTCHA")

                submitted = st.form_submit_button("Reset Password")

                # Password validation function
                def validate_password(password):
                    password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_])[^\s]{8,}$'
                    return re.match(password_pattern, password)

                if submitted:
                    if new_password and captcha_input:
                        if captcha_input.strip() != st.session_state.captcha_text:
                            st.warning("❌ CAPTCHA did not match. Please try again.")
                            st.session_state.refresh_captcha = False
                        elif validate_password(new_password):
                            success = reset_password(token, new_password)
                            if success:
                                st.session_state.password_reset_success = True
                                st.rerun()
                            else:
                                st.error("❌ Invalid or expired reset link.")
                        else:
                            st.warning("⚠️ Please meet all the password criteria.")
                    else:
                        st.warning("Please enter a new password and CAPTCHA.")

    # Add bottom vertical spacing
    for _ in range(4):
        st.empty()
