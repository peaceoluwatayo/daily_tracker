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
import re

# Validate Username
def is_valid_username(username):
    return re.match(r"^[A-Z][A-Za-z0-9_]{5,}$", username) is not None  # Starts with a capital letter and no spaces

# Validate Password
def is_valid_password(password):
    return (
        len(password) >= 8 and
        re.search(r"[A-Za-z]", password) and  # At least one letter
        re.search(r"[0-9]", password) and     # At least one number
        re.search(r"[\W_]", password) and     # At least one special character
        re.search(r"[A-Z]", password) and     # At least one capital letter
        " " not in password                   # No spaces
    )

def show_signup():
    for _ in range(6):
        st.empty()

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
            if new_user:
                st.markdown("**Username Requirements:**")
                st.markdown("- ✅ Starts with a capital letter" if re.match(r"^[A-Z]", new_user) else "- ❌ Starts with a capital letter")
                st.markdown("- ✅ At least 6 characters" if len(new_user) >= 6 else "- ❌ At least 6 characters")
                st.markdown("- ✅ No spaces" if " " not in new_user else "- ❌ No spaces")
                st.markdown("- ✅ Only letters, numbers, or underscores" if re.match(r"^[A-Za-z0-9_]+$", new_user) else "- ❌ Only letters, numbers, or underscores")

            new_pass = st.text_input("Choose a password", type="password")
            if new_pass:
                st.markdown("**Password Requirements:**")
                st.markdown("- ✅ At least 8 characters" if len(new_pass) >= 8 else "- ❌ At least 8 characters")
                st.markdown("- ✅ At least one letter" if re.search(r"[A-Za-z]", new_pass) else "- ❌ At least one letter")
                st.markdown("- ✅ At least one capital letter" if re.search(r"[A-Z]", new_pass) else "- ❌ At least one capital letter")
                st.markdown("- ✅ At least one number" if re.search(r"\d", new_pass) else "- ❌ At least one number")
                st.markdown("- ✅ At least one special character" if re.search(r"[\W_]", new_pass) else "- ❌ At least one special character")
                st.markdown("- ✅ No spaces" if " " not in new_pass else "- ❌ No spaces")

            email = st.text_input("Enter your email address")

            if st.button("Sign Up"):
                if new_user and new_pass and email:
                    if not is_valid_username(new_user):
                        st.warning("⚠️ Invalid username. Please follow all the listed criteria.")
                    elif not is_valid_password(new_pass):
                        st.warning("⚠️ Invalid password. Please follow all the listed criteria.")
                    else:
                        success, token = add_user(new_user, new_pass, email)
                        if success:
                            send_confirmation_email(email, new_user, token)
                        else:
                            st.warning("⚠️ Username or email already exists.")
                else:
                    st.warning("Please fill in all fields.")

            if st.button("Back to Login"):
                st.session_state.page = "login"
                st.rerun()

    for _ in range(4):
        st.empty()
