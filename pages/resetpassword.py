import streamlit as st
from database import reset_password

def show_reset_password(token):
    st.title("🔑 Set New Password")

    new_password = st.text_input("Enter New Password", type="password")

    if st.button("Reset Password"):
        if new_password:
            success = reset_password(token, new_password)
            if success:
                st.success("✅ Your password has been successfully reset.")
                st.info("You can now log in with your new password.")
            else:
                st.error("❌ Invalid or expired reset link.")
        else:
            st.warning("Please enter a new password.")
