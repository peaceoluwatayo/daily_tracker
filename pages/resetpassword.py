# import streamlit as st
# from database import reset_password

# def show_reset_password(token):
#     st.title("🔑 Set New Password")

#     new_password = st.text_input("Enter New Password", type="password")

#     if st.button("Reset Password"):
#         if new_password:
#             success = reset_password(token, new_password)
#             if success:
#                 st.success("✅ Your password has been successfully reset.")
#                 st.info("You can now log in with your new password.")
#             else:
#                 st.error("❌ Invalid or expired reset link.")
#         else:
#             st.warning("Please enter a new password.")




import streamlit as st
from database import reset_password

def show_reset_password(token):
    # st.set_page_config(page_title="Reset Password", layout="centered")

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
                    <h2>🔑 Set New Password</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

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

    # Add bottom vertical spacing
    for _ in range(4):
        st.empty()
