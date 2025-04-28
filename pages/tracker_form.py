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
       "Choose an option", "Excited", "Happy", "Contented", "Low", "Depressed"
    ])

    food_choices = st.multiselect("2. What did you eat today? (Select all that apply)", [
        "Breakfast - Health balanced (Fruit & Veg)",
        "Breakfast - Easy food/Snacks",
        "Breakfast - I didn't have breakfast today",
        "Lunch - Health balanced (Fruit & Veg)",
        "Lunch - Easy food/Snacks",
        "Lunch - I didn't have lunch today",
        "Dinner - Health balanced (Fruit & Veg)",
        "Dinner - Easy food/Snacks",
        "Dinner - I didn't have dinner today"
    ])
    
    water = st.selectbox("3. How was your water intake today?", [
        "Choose an option", "Adequate (>1 litre)", "Low (<1 litre)"
    ])

    exercise = st.selectbox("4. Did you exercise today?", [
        "Choose an option", "Gym", "Cycle", "Run", "Walk", "I didn't exercise today"
    ])

    social_choices = st.multiselect("5. Did you socialise today? (Select all that apply)", [
        "Family - In Person",
        "Family - By Phone",
        "Family - By Text/Message",
        "Family - I didn't socialize with family today",
        "Friends - In Person",
        "Friends - By Phone",
        "Friends - By Text/Message",
        "Friends - I didn't socialize with friends today",
        "Neighbour - In Person",
        "Neighbour - By Phone",
        "Neighbour - By Text/Message",
        "Neighbour - I didn't socialize with neighbour today",
        "Stranger - In Person",
        "Stranger -  By Phone",
        "Stranger -  By Text/Message",
        "Stranger - I didn't socialize with stranger today"
    ])

    sleep_quality = st.selectbox("6. How was your sleep last night?", [
        "Choose an option", "Excellent", "Good", "Average", "Poor", "Very poor"
    ])

    sleep_time = st.selectbox("7. What time did you go to sleep last night?", [
        "Choose an option", "9pm", "10pm", "11pm", "Midnight", "After Midnight"
    ])

    sleep_duration = st.selectbox("8. How many hours of sleep did you get last night?", [
        "Choose an option", "Less than 3 hours", "3-4 hours", "5-6 hours", "7-8 hours", "8+ hours"
    ])
    
    # Convert lists into comma-separated strings
    food_str = ", ".join(food_choices)
    social_str = ", ".join(social_choices)

    # Collecting all inputs into an entry dictionary
    entry = {
        "username": username,
        "mood": mood,
        "food": food_str,
        "water": water,
        "exercise": exercise,
        "social": social_str,
        "sleep_quality": sleep_quality,
        "sleep_time": sleep_time,
        "sleep_duration": sleep_duration
    }

    # --- Validation Rules ---

    # 1. Check that no field is "Choose an option"
    basic_validation = "Choose an option" not in entry.values()

    # 2. Food validation: breakfast, lunch, dinner must be selected
    breakfast_selected = any("Breakfast" in item for item in food_choices)
    lunch_selected = any("Lunch" in item for item in food_choices)
    dinner_selected = any("Dinner" in item for item in food_choices)

    food_validation = breakfast_selected and lunch_selected and dinner_selected

    # 3. Social validation: must select Family, Friends, Neighbour, Stranger
    family_selected = any("Family" in item for item in social_choices)
    friends_selected = any("Friends" in item for item in social_choices)
    neighbour_selected = any("Neighbour" in item for item in social_choices)
    stranger_selected = any("Stranger" in item for item in social_choices)

    social_validation = family_selected and friends_selected and neighbour_selected and stranger_selected

    if st.button("Submit Entry"):
        if not basic_validation:
            st.warning("Please answer all questions before submitting.")
        elif not food_validation:
            st.warning("Please select an option for Breakfast, Lunch, and Dinner.")
        elif not social_validation:
            st.warning("Please select at least one option for Family, Friends, Neighbour, and Stranger.")
        else:
            save_entry_to_db(entry)
            st.success("Entry submitted successfully!")
            st.rerun()
