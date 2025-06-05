# # Not centered
# import streamlit as st
# from database import add_user
# from utils.email_utils import send_confirmation_email

# def show_signup():
#     st.title("🆕 Create New Account")

#     new_user = st.text_input("Choose a username")
#     new_pass = st.text_input("Choose a password", type="password")
#     email = st.text_input("Enter your email address")

#     if st.button("Sign Up"):
#         if new_user and new_pass and email:
#             success, token = add_user(new_user, new_pass, email)
#             if success:
#                 send_confirmation_email(email, new_user, token)
#             else:
#                 st.warning("⚠️ Username or email already exists.")
#         else:
#             st.warning("Please fill in all fields.")

#     if st.button("Back to Login"):
#         st.session_state.page = "login"
#         st.rerun()




# # Without captcha
# import streamlit as st
# from database import add_user
# from utils.email_utils import send_confirmation_email
# import re

# # Validate Username
# def is_valid_username(username):
#     return re.match(r"^[A-Z][A-Za-z0-9_]{5,}$", username) is not None  # Starts with a capital letter and no spaces

# # Validate Password
# def is_valid_password(password):
#     return (
#         len(password) >= 8 and
#         re.search(r"[A-Za-z]", password) and  # At least one letter
#         re.search(r"[0-9]", password) and     # At least one number
#         re.search(r"[\W_]", password) and     # At least one special character
#         re.search(r"[A-Z]", password) and     # At least one capital letter
#         " " not in password                   # No spaces
#     )

# def show_signup():
#     for _ in range(6):
#         st.empty()

#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         with st.container():
#             st.markdown(
#                 """
#                 <div style="text-align: center;">
#                     <h2>🆕 Create New Account</h2>
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )

#             new_user = st.text_input("Choose a username")
#             if new_user:
#                 st.markdown("**Username Requirements:**")
#                 st.markdown("- ✅ Starts with a capital letter" if re.match(r"^[A-Z]", new_user) else "- ❌ Starts with a capital letter")
#                 st.markdown("- ✅ At least 6 characters" if len(new_user) >= 6 else "- ❌ At least 6 characters")
#                 st.markdown("- ✅ No spaces" if " " not in new_user else "- ❌ No spaces")
#                 st.markdown("- ✅ Only letters, numbers, or underscores" if re.match(r"^[A-Za-z0-9_]+$", new_user) else "- ❌ Only letters, numbers, or underscores")

#             new_pass = st.text_input("Choose a password", type="password")
#             if new_pass:
#                 st.markdown("**Password Requirements:**")
#                 st.markdown("- ✅ At least 8 characters" if len(new_pass) >= 8 else "- ❌ At least 8 characters")
#                 st.markdown("- ✅ At least one letter" if re.search(r"[A-Za-z]", new_pass) else "- ❌ At least one letter")
#                 st.markdown("- ✅ At least one capital letter" if re.search(r"[A-Z]", new_pass) else "- ❌ At least one capital letter")
#                 st.markdown("- ✅ At least one number" if re.search(r"\d", new_pass) else "- ❌ At least one number")
#                 st.markdown("- ✅ At least one special character" if re.search(r"[\W_]", new_pass) else "- ❌ At least one special character")
#                 st.markdown("- ✅ No spaces" if " " not in new_pass else "- ❌ No spaces")

#             email = st.text_input("Enter your email address")

#             if st.button("Sign Up"):
#                 if new_user and new_pass and email:
#                     if not is_valid_username(new_user):
#                         st.warning("⚠️ Invalid username. Please follow all the listed criteria.")
#                     elif not is_valid_password(new_pass):
#                         st.warning("⚠️ Invalid password. Please follow all the listed criteria.")
#                     else:
#                         success, token = add_user(new_user, new_pass, email)
#                         if success:
#                             send_confirmation_email(email, new_user, token)
#                         else:
#                             st.warning("⚠️ Username or email already exists.")
#                 else:
#                     st.warning("Please fill in all fields.")

#             if st.button("Back to Login"):
#                 st.session_state.page = "login"
#                 st.rerun()

#     for _ in range(4):
#         st.empty()



import streamlit as st
import re
import random
import string
from captcha.image import ImageCaptcha
from io import BytesIO
from PIL import Image
from database import add_user
from utils.email_utils import send_confirmation_email

# Validate Username
def is_valid_username(username):
    return (
        len(username) >= 6 and
        username[0].isupper() and
        " " not in username and
        re.match(r"^[A-Za-z0-9_]+$", username)
    )

# Validate Password
def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[\W_]", password):
        return False
    if " " in password:
        return False
    return True

# Generate CAPTCHA
def generate_captcha_text(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Show Signup Page
def show_signup():
    for _ in range(6):
        st.empty()

    if 'captcha_text' not in st.session_state or st.session_state.get('refresh_captcha', True):
        st.session_state.captcha_text = generate_captcha_text()
        st.session_state.refresh_captcha = False

    if st.session_state.get('account_created', False):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.success("✅ Email verification sent. Please check your inbox to verify your account.")
            if st.button("Back to Login"):
                st.session_state.page = "login"
                st.session_state.account_created = False
                st.rerun()
        return

    image = ImageCaptcha(width=280, height=90)
    captcha_text = st.session_state.captcha_text
    buffer = BytesIO()
    image.generate_image(captcha_text).save(buffer, format="PNG")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            st.markdown("<div style='text-align: center;'><h2>🆕 Create New Account</h2></div>", unsafe_allow_html=True)

            with st.form("signup_form", clear_on_submit=False):
                new_user = st.text_input("Choose a username")
                # Show instructions always
                st.markdown(
                    '<p style="font-size: medium; color: gray;">Username must start with a capital letter, have at least 6 characters, contain no spaces, and only use letters, numbers, or underscores.</p>',
                    unsafe_allow_html=True
                )

                new_pass = st.text_input("Choose a password", type="password")
                # Show instructions always
                st.markdown(
                    '<p style="font-size: medium; color: gray;">Password must be at least 8 characters with a capital letter, lowercase letter, number, special character, and no spaces.</p>',
                    unsafe_allow_html=True
                )

                email = st.text_input("Enter your email address")

                st.image(buffer.getvalue(), caption="Enter the CAPTCHA text above")
                captcha_input = st.text_input("Enter CAPTCHA")

                submitted = st.form_submit_button("Sign Up")

                if submitted:
                    if new_user and new_pass and email and captcha_input:
                        if captcha_input.strip() != st.session_state.captcha_text:
                            st.error("❌ CAPTCHA did not match. Please try again.")
                            st.session_state.refresh_captcha = False
                        elif not is_valid_username(new_user):
                            st.warning("⚠️ Invalid username. Please follow the instructions under the field.")
                        elif not is_valid_password(new_pass):
                            st.warning("⚠️ Invalid password. Please follow the instructions under the field.")
                        else:
                            success, token = add_user(new_user, new_pass, email)
                            if success:
                                send_confirmation_email(email, new_user, token)
                                st.session_state.account_created = True
                                st.rerun()
                            else:
                                st.warning("⚠️ Username or email already exists.")
                    else:
                        st.warning("Please fill in all fields, including the CAPTCHA.")

    for _ in range(4):
        st.empty()
