# # Not centered
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



# # Without captcha
# import streamlit as st
# from database import authenticate_user

# def show_login():
#     # st.set_page_config(page_title="Login", layout="centered")

#     # Add vertical spacing to center the content
#     for _ in range(6):
#         st.empty()

#     # Create centered column layout
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         with st.container():
#             st.markdown(
#                 """
#                 <div style="text-align: center;">
#                     <h2>📘 Daily Journal Tracker</h2>
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )

#             username = st.text_input("Username")
#             password = st.text_input("Password", type="password")

#             if st.button("Login"):
#                 if username and password:
#                     result = authenticate_user(username, password)
#                     if result == "unverified":
#                         st.warning("⚠️ Please verify your email before logging in.")
#                     elif result == "success":
#                         st.session_state.logged_in = True
#                         st.session_state.username = username
#                         st.session_state.page = "first"
#                         st.rerun()
#                     else:
#                         st.error("❌ Invalid username or password.")
#                 else:
#                     st.warning("Please enter both username and password.")

#             col_a, col_b = st.columns(2)
#             with col_a:
#                 if st.button("Sign Up"):
#                     st.session_state.page = "signup"
#                     st.rerun()
#             with col_b:
#                 if st.button("Forgot Password?"):
#                     st.session_state.page = "forgot_password"
#                     st.rerun()

#     # Add vertical spacing after the form
#     for _ in range(4):
#         st.empty()




# With captcha
import streamlit as st
import re
import random
import string
from captcha.image import ImageCaptcha
from io import BytesIO
from database import authenticate_user

# Generate random CAPTCHA text
def generate_captcha_text(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def show_login():
    # Add vertical spacing to center the content
    for _ in range(6):
        st.empty()

    # Initialize CAPTCHA in session state if not already initialized
    if 'captcha_text' not in st.session_state:
        st.session_state.captcha_text = generate_captcha_text()

    # Generate CAPTCHA image in memory
    image = ImageCaptcha(width=280, height=90)
    captcha_image = image.generate(st.session_state.captcha_text)
    captcha_bytes = BytesIO(captcha_image.read())

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

            # CAPTCHA display
            st.image(captcha_bytes, caption="Enter the CAPTCHA text above")
            captcha_input = st.text_input("Enter CAPTCHA")

            if st.button("Login"):
                # Check if the CAPTCHA input is correct (case-sensitive)
                if username and password and captcha_input:
                    if captcha_input.strip() != st.session_state.captcha_text:
                        # Display an error message for incorrect CAPTCHA
                        st.error("❌ CAPTCHA did not match. Please try again.")
                    else:
                        # If CAPTCHA matches, continue with authentication
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
                    st.warning("Please enter both username and password, and solve the CAPTCHA.")

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
