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


import streamlit as st
from database import add_user
from utils.email_utils import send_confirmation_email

def show_signup():
    # st.set_page_config(page_title="Sign Up", layout="centered")

    # Add vertical spacing
    for _ in range(6):
        st.empty()

    # Center content horizontally
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            st.markdown(
                """
                <div style="text-align: center;">
                    <h2>🆕 Create New Account</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

            new_user = st.text_input("Choose a username")
            new_pass = st.text_input("Choose a password", type="password")
            email = st.text_input("Enter your email address")

            if st.button("Sign Up"):
                if new_user and new_pass and email:
                    success, token = add_user(new_user, new_pass, email)
                    if success:
                        send_confirmation_email(email, new_user, token)
                        st.success("✅ Account created! Please check your email to verify.")
                    else:
                        st.warning("⚠️ Username or email already exists.")
                else:
                    st.warning("Please fill in all fields.")

            if st.button("Back to Login"):
                st.session_state.page = "login"
                st.rerun()

    # Add vertical spacing after form
    for _ in range(4):
        st.empty()
