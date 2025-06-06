# # Not centered
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



# # without captcha
# import streamlit as st
# import re
# from database import reset_password

# def show_reset_password(token):
#     # Add vertical spacing
#     for _ in range(6):
#         st.empty()

#     # Center content horizontally
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         with st.container():
#             st.markdown(
#                 """
#                 <div style="text-align: center;">
#                     <h2>🔑 Set New Password</h2>
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )

#             new_password = st.text_input("Enter New Password", type="password")

#             # Define password criteria
#             def validate_password(password):
#                 # Password must include at least one capital letter, one letter, one number, one special character, and at least 8 characters
#                 password_pattern = r'^(?=.*[A-Za-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
#                 return re.match(password_pattern, password)

#             # Show password criteria dynamically
#             if new_password:
#                 criteria_met = []
#                 # Check if criteria are met and provide feedback
#                 if len(new_password) >= 8:
#                     criteria_met.append("✅ At least 8 characters")
#                 else:
#                     criteria_met.append("❌ At least 8 characters")

#                 if re.search(r'[A-Za-z]', new_password):
#                     criteria_met.append("✅ Contains at least one letter")
#                 else:
#                     criteria_met.append("❌ Contains at least one letter")

#                 if re.search(r'[A-Z]', new_password):
#                     criteria_met.append("✅ Contains at least one capital letter")
#                 else:
#                     criteria_met.append("❌ Contains at least one capital letter")

#                 if re.search(r'\d', new_password):
#                     criteria_met.append("✅ Contains at least one number")
#                 else:
#                     criteria_met.append("❌ Contains at least one number")

#                 if re.search(r'[@$!%*?&]', new_password):
#                     criteria_met.append("✅ Contains at least one special character")
#                 else:
#                     criteria_met.append("❌ Contains at least one special character")

#                 # Display the criteria messages
#                 for criterion in criteria_met:
#                     st.markdown(criterion)

#             if st.button("Reset Password"):
#                 if new_password:
#                     if validate_password(new_password):
#                         success = reset_password(token, new_password)
#                         if success:
#                             st.success("✅ Your password has been successfully reset.")
#                             st.info("You can now log in with your new password.")
#                         else:
#                             st.error("❌ Invalid or expired reset link.")
#                     else:
#                         st.warning("⚠️ Please meet all the password criteria.")
#                 else:
#                     st.warning("Please enter a new password.")

#     # Add bottom vertical spacing
#     for _ in range(4):
#         st.empty()




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
