import streamlit as st
from database import save_entry_to_db, has_filled_form_today

def show_tracker_form():
    st.title("📝 Daily Tracker Form")

    # Place Back to Home on the left and Logout on the right
    col1, col2 = st.columns([8, 1])
    with col1:
        if st.button("Back to Home"):
            st.session_state.page = "first"  # or "home" depending on your app
            st.rerun()
    with col2:
        if st.button("Logout"):
            st.session_state.clear()
            st.session_state.page = "login"
            st.rerun()

    # Form inputs
    mood = st.selectbox("1. How are you feeling today?", [
        "Excited", "Happy", "Contented", "Low", "Depressed"
    ])

    breakfast = st.selectbox("2. What did you eat for breakfast today?", [
        "Healthy balanced", "Easy food/Snacks"
    ])

    lunch = st.selectbox("3. What did you eat for lunch today?", [
        "Healthy balanced", "Easy food/Snacks"
    ])

    dinner = st.selectbox("4. What did you eat for dinner today?", [
        "Healthy balanced", "Easy food/Snacks"
    ])

    water = st.selectbox("5. How was your water intake today?", [
        "Adequate (>1 litre)", "Low (<1 litre)"
    ])

    exercise = st.selectbox("6. Did you exercise today?", [
        "Gym", "Cycle", "Run", "Walk", "I didn't exercise today"
    ])

    family_social = st.selectbox("7. How did you socialize with family today?", [
        "In person", "By Phone", "By Text/Message"
    ])

    friend_social = st.selectbox("8. How did you socialize with friends today?", [
        "In person", "By Phone", "By Text/Message"
    ])

    neighbour_social = st.selectbox("9. How did you socialize with neighbours today?", [
        "In person", "By Phone", "By Text/Message"
    ])

    stranger_social = st.selectbox("10. How did you socialize with strangers today?", [
        "In person", "By Phone", "By Text/Message"
    ])

    sleep_quality = st.selectbox("11. How was your sleep last night?", [
        "Excellent", "Good", "Average", "Poor", "Very poor"
    ])

    sleep_time = st.selectbox("12. What time did you go to bed last night?", [
        "9pm", "10pm", "11pm", "Midnight", "After Midnight"
    ])

    sleep_duration = st.selectbox("13. How many hours of sleep did you get last night?", [
        "Less than 3 hours", "3-4 hours", "5-6 hours", "7-8 hours", "8+ hours"
    ])

    if has_filled_form_today(st.session_state['username']):
        st.warning("You have already submitted your form for today!")
    else:
        if st.button("Submit Entry"):
            entry = {
                "username": st.session_state.get("username"),
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

          
            save_entry_to_db(entry)
            st.success("Entry submitted successfully!")

            # Automatically mark as filled for today to prevent resubmission
            st.session_state['has_filled_form'] = True
