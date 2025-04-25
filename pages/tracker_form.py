import streamlit as st
from database import save_entry_to_db, has_filled_form_today

def show_tracker_form():
    st.title("📝 Daily Tracker Form")

    # Place Back to Home on the left and Logout on the right
    col1, col2 = st.columns([8, 1])
    with col1:
        if st.button("Back to Home"):
            st.session_state.page = "first"
            st.rerun()
    with col2:
        if st.button("Logout"):
            st.session_state.clear()
            st.session_state.page = "login"
            st.rerun()

    username = st.session_state.get("username")

    if has_filled_form_today(username):
        st.warning("You have already submitted your form for today!")
        return  # Exit early — don't show the form

    # --- Only shows if user hasn't filled the form today ---
    mood = st.selectbox("1. How are you feeling today?", [
       "Select an option", "Excited", "Happy", "Contented", "Low", "Depressed"
    ])

    breakfast = st.selectbox("2. What did you eat for breakfast today?", [
        "Select an option", "Healthy balanced", "Easy food/Snacks"
    ])

    lunch = st.selectbox("3. What did you eat for lunch today?", [
        "Select an option", "Healthy balanced", "Easy food/Snacks"
    ])

    dinner = st.selectbox("4. What did you eat for dinner today?", [
        "Select an option", "Healthy balanced", "Easy food/Snacks"
    ])

    water = st.selectbox("5. How was your water intake today?", [
        "Select an option", "Adequate (>1 litre)", "Low (<1 litre)"
    ])

    exercise = st.selectbox("6. Did you exercise today?", [
        "Select an option", "Gym", "Cycle", "Run", "Walk", "I didn't exercise today"
    ])

    family_social = st.selectbox("7. How did you socialize with family today?", [
        "Select an option", "In Person", "By Phone", "By Text/Message"
    ])

    friend_social = st.selectbox("8. How did you socialize with friends today?", [
        "Select an option","In Person", "By Phone", "By Text/Message"
    ])

    neighbour_social = st.selectbox("9. How did you socialize with neighbours today?", [
        "Select an option", "In Person", "By Phone", "By Text/Message"
    ])

    stranger_social = st.selectbox("10. How did you socialize with strangers today?", [
        "Select an option", "In Person", "By Phone", "By Text/Message"
    ])

    sleep_quality = st.selectbox("11. How was your sleep last night?", [
        "Select an option", "Excellent", "Good", "Average", "Poor", "Very poor"
    ])

    sleep_time = st.selectbox("12. What time did you go to bed last night?", [
        "Select an option", "9pm", "10pm", "11pm", "Midnight", "After Midnight"
    ])

    sleep_duration = st.selectbox("13. How many hours of sleep did you get last night?", [
        "Select an option", "Less than 3 hours", "3-4 hours", "5-6 hours", "7-8 hours", "8+ hours"
    ])

     # Collecting all inputs into an entry dictionary
    entry = {
        "username": username,
        "mood": mood,
        "breakfast": breakfast,
        "lunch": lunch,
        "dinner": dinner,
        "water": water,
        "exercise": exercise,
        "family_social": family_social,
        "friend_social": friend_social,
        "neighbour_social": neighbour_social,
        "stranger_social": stranger_social,
        "sleep_quality": sleep_quality,
        "sleep_time": sleep_time,
        "sleep_duration": sleep_duration
    }

    # Validation: Check if any question is still at "Select an option"
    if "Select an option" in entry.values():
        st.warning("Please answer all questions before submitting.")
    else:
        if st.button("Submit Entry"):
            save_entry_to_db(entry)
            st.success("Entry submitted successfully!")

            # Optionally rerun to hide the form after successful submission
            st.rerun()