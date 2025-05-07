# import streamlit as st
# from database import save_entry_to_db, save_scores_to_db, has_filled_form_today

# def show_tracker_form():
#     st.markdown("<h1 style='text-align: center;'>📝 Daily Tracker Form</h1>", unsafe_allow_html=True)

#     col1, col2 = st.columns([8, 1])
#     with col1:
#         if st.button("Back to Home"):
#             st.session_state.page = "first"
#             st.rerun()
#     with col2:
#         if st.button("Logout"):
#             st.session_state.clear()
#             st.session_state.page = "login"
#             st.rerun()

#     username = st.session_state.get("username")
#     if has_filled_form_today(username):
#         st.warning("You have already submitted your form for today!")
#         return

#     # ---------- FORM QUESTIONS ----------
#     def styled_question(question_text):
#         st.markdown(f"<div style='font-size:22px; font-weight:bold;'>{question_text}</div>"
#                     "<div style='margin-left: 20px; font-size:14px;'>", unsafe_allow_html=True)

#     def close_div():
#         st.markdown("</div>", unsafe_allow_html=True)

#     styled_question("1. How are you feeling today?")
#     mood = st.selectbox("", ["Choose an option", "Excited", "Happy", "Contented", "Low", "Depressed"])
#     close_div()

#     styled_question("2. What did you eat today? (Select all that apply)")
#     food_choices = st.multiselect("", [
#         "Breakfast - Health balanced (Fruit & Veg)",
#         "Breakfast - Easy food/Snacks",
#         "Breakfast - I didn't have breakfast today",
#         "Lunch - Health balanced (Fruit & Veg)",
#         "Lunch - Easy food/Snacks",
#         "Lunch - I didn't have lunch today",
#         "Dinner - Health balanced (Fruit & Veg)",
#         "Dinner - Easy food/Snacks",
#         "Dinner - I didn't have dinner today"
#     ])
#     close_div()

#     styled_question("3. How was your water intake today?")
#     water = st.selectbox("", ["Choose an option", "Adequate (>1 litre)", "Low (<1 litre)"])
#     close_div()

#     styled_question("4. Did you exercise today?")
#     exercise = st.selectbox("", ["Choose an option", "Gym", "Cycle", "Run", "Walk", "I didn't exercise today"])
#     close_div()

#     styled_question("5. Did you socialise today? (Select all that apply)")
#     social_choices = st.multiselect("", [
#         "Family - In Person", "Family - By Phone", "Family - By Text/Message", "Family - I didn't socialize with family today",
#         "Friends - In Person", "Friends - By Phone", "Friends - By Text/Message", "Friends - I didn't socialize with friends today",
#         "Neighbour - In Person", "Neighbour - By Phone", "Neighbour - By Text/Message", "Neighbour - I didn't socialize with neighbour today",
#         "Stranger - In Person", "Stranger - By Phone", "Stranger - By Text/Message", "Stranger - I didn't socialize with stranger today"
#     ])
#     close_div()

#     styled_question("6. How was your sleep last night?")
#     sleep_quality = st.selectbox("", ["Choose an option", "Excellent", "Good", "Average", "Poor", "Very poor"])
#     close_div()

#     styled_question("7. What time did you go to sleep last night?")
#     sleep_time = st.selectbox("", ["Choose an option", "9pm", "10pm", "11pm", "Midnight", "After Midnight"])
#     close_div()

#     styled_question("8. How many hours of sleep did you get last night?")
#     sleep_duration = st.selectbox("", ["Choose an option", "Less than 3 hours", "3-4 hours", "5-6 hours", "7-8 hours", "8+ hours"])
#     close_div()

#     # ---------- VALIDATION ----------
#     food_str = ", ".join(food_choices)
#     social_str = ", ".join(social_choices)

#     entry = {
#         "username": username,
#         "mood": mood,
#         "food": food_str,
#         "water": water,
#         "exercise": exercise,
#         "social": social_str,
#         "sleep_quality": sleep_quality,
#         "sleep_time": sleep_time,
#         "sleep_duration": sleep_duration
#     }

#     basic_validation = "Choose an option" not in entry.values()

#     breakfast_selected = any("Breakfast" in item for item in food_choices)
#     lunch_selected = any("Lunch" in item for item in food_choices)
#     dinner_selected = any("Dinner" in item for item in food_choices)
#     food_validation = breakfast_selected and lunch_selected and dinner_selected

#     family_selected = any("Family" in item for item in social_choices)
#     friends_selected = any("Friends" in item for item in social_choices)
#     neighbour_selected = any("Neighbour" in item for item in social_choices)
#     stranger_selected = any("Stranger" in item for item in social_choices)
#     social_validation = family_selected and friends_selected and neighbour_selected and stranger_selected

#     if st.button("Submit Entry"):
#         if not basic_validation:
#             st.warning("Please answer all questions before submitting.")
#             return
#         elif not food_validation:
#             st.warning("Please select an option for Breakfast, Lunch, and Dinner.")
#             return
#         elif not social_validation:
#             st.warning("Please select at least one option for Family, Friends, Neighbour, and Stranger.")
#             return

#         entry_id = save_entry_to_db(entry)

#         mood_scores = {"Excited": 2, "Happy": 1, "Contented": 0, "Low": -1, "Depressed": -2}
#         food_scores = {
#             "Breakfast - Health balanced (Fruit & Veg)": 1,
#             "Breakfast - Easy food/Snacks": -1,
#             "Breakfast - I didn't have breakfast today": 0,
#             "Lunch - Health balanced (Fruit & Veg)": 1,
#             "Lunch - Easy food/Snacks": -1,
#             "Lunch - I didn't have lunch today": 0,
#             "Dinner - Health balanced (Fruit & Veg)": 1,
#             "Dinner - Easy food/Snacks": -1,
#             "Dinner - I didn't have dinner today": 0
#         }
#         water_scores = {"Adequate (>1 litre)": 1, "Low (<1 litre)": -1}
#         exercise_scores = {"Gym": 1, "Cycle": 1, "Run": 1, "Walk": 1, "I didn't exercise today": -1}
#         social_scores = {
#             "Family - In Person": 3, "Family - By Phone": 2, "Family - By Text/Message": 1,
#             "Family - I didn't socialize with family today": -1,
#             "Friends - In Person": 3, "Friends - By Phone": 2, "Friends - By Text/Message": 1,
#             "Friends - I didn't socialize with friends today": -1,
#             "Neighbour - In Person": 3, "Neighbour - By Phone": 2, "Neighbour - By Text/Message": 1,
#             "Neighbour - I didn't socialize with neighbour today": -1,
#             "Stranger - In Person": 3, "Stranger - By Phone": 2, "Stranger - By Text/Message": 1,
#             "Stranger - I didn't socialize with stranger today": -1
#         }
#         sleep_quality_scores = {"Excellent": 5, "Good": 4, "Average": 3, "Poor": 2, "Very poor": 1}
#         sleep_time_scores = {"9pm": 5, "10pm": 4, "11pm": 3, "Midnight": 2, "After Midnight": 1}
#         sleep_duration_scores = {
#             "Less than 3 hours": 1, "3-4 hours": 2, "5-6 hours": 3, "7-8 hours": 4, "8+ hours": 5
#         }

#         mood_score = mood_scores.get(mood, 0)
#         food_score = sum([food_scores.get(f, 0) for f in food_choices])
#         water_score = water_scores.get(water, 0)
#         exercise_score = exercise_scores.get(exercise, 0)
#         social_score = sum([social_scores.get(s, 0) for s in social_choices])
#         sleep_quality_score = sleep_quality_scores.get(sleep_quality, 0)
#         sleep_time_score = sleep_time_scores.get(sleep_time, 0)
#         sleep_duration_score = sleep_duration_scores.get(sleep_duration, 0)

#         scores = {
#             "entry_id": entry_id,
#             "username": username,
#             "mood_score": mood_score,
#             "food_score": food_score,
#             "water_score": water_score,
#             "exercise_score": exercise_score,
#             "social_score": social_score,
#             "sleep_quality_score": sleep_quality_score,
#             "sleep_time_score": sleep_time_score,
#             "sleep_duration_score": sleep_duration_score
#         }

#         save_scores_to_db(scores)
#         st.success("Entry submitted successfully!")
#         st.rerun()





import streamlit as st
from database import save_entry_to_db, save_scores_to_db, has_filled_form_today

def show_tracker_form():
    st.markdown("<h1 style='text-align: center;'>📝 Daily Tracker Form</h1>", unsafe_allow_html=True)

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
        return

    def render_question(question, widget_type="selectbox", options=None):
        # Increase the font size for the question and set a smaller font for the options
        col1, col2 = st.columns([3.5, 4.5])
        with col1:
            st.markdown(f"<span style='font-size:20px; font-weight:bold;'>{question}</span>", unsafe_allow_html=True)
        with col2:
            if widget_type == "selectbox":
                return st.selectbox(" ", options, label_visibility="collapsed", key=question)
            elif widget_type == "multiselect":
                return st.multiselect(" ", options, label_visibility="collapsed", key=question)

    # ---------- FORM QUESTIONS ----------
    mood = render_question("1. How are you feeling today?", "selectbox", 
        ["Choose an option", "Excited", "Happy", "Contented", "Low", "Depressed"])

    food_choices = render_question("2. What did you eat today? (Select all that apply)", "multiselect", [
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

    water = render_question("3. How was your water intake today?", "selectbox",
        ["Choose an option", "Adequate (>1 litre)", "Low (<1 litre)"])

    exercise = render_question("4. Did you exercise today?", "selectbox",
        ["Choose an option", "Gym", "Cycle", "Run", "Walk", "I didn't exercise today"])

    social_choices = render_question("5. Did you socialise today? (Select all that apply)", "multiselect", [
        "Family - In Person", "Family - By Phone", "Family - By Text/Message", "Family - I didn't socialize with family today",
        "Friends - In Person", "Friends - By Phone", "Friends - By Text/Message", "Friends - I didn't socialize with friends today",
        "Neighbour - In Person", "Neighbour - By Phone", "Neighbour - By Text/Message", "Neighbour - I didn't socialize with neighbour today",
        "Stranger - In Person", "Stranger - By Phone", "Stranger - By Text/Message", "Stranger - I didn't socialize with stranger today"
    ])

    sleep_quality = render_question("6. How was your sleep last night?", "selectbox",
        ["Choose an option", "Excellent", "Good", "Average", "Poor", "Very poor"])

    sleep_time = render_question("7. What time did you go to sleep last night?", "selectbox",
        ["Choose an option", "9pm", "10pm", "11pm", "Midnight", "After Midnight"])

    sleep_duration = render_question("8. How many hours of sleep did you get last night?", "selectbox",
        ["Choose an option", "Less than 3 hours", "3-4 hours", "5-6 hours", "7-8 hours", "8+ hours"])

    # ---------- VALIDATION ----------
    food_str = ", ".join(food_choices)
    social_str = ", ".join(social_choices)

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

    basic_validation = "Choose an option" not in entry.values()

    breakfast_selected = any("Breakfast" in item for item in food_choices)
    lunch_selected = any("Lunch" in item for item in food_choices)
    dinner_selected = any("Dinner" in item for item in food_choices)
    food_validation = breakfast_selected and lunch_selected and dinner_selected

    family_selected = any("Family" in item for item in social_choices)
    friends_selected = any("Friends" in item for item in social_choices)
    neighbour_selected = any("Neighbour" in item for item in social_choices)
    stranger_selected = any("Stranger" in item for item in social_choices)
    social_validation = family_selected and friends_selected and neighbour_selected and stranger_selected

    if st.button("Submit Entry"):
        if not basic_validation:
            st.warning("Please answer all questions before submitting.")
            return
        elif not food_validation:
            st.warning("Please select an option for Breakfast, Lunch, and Dinner.")
            return
        elif not social_validation:
            st.warning("Please select at least one option for Family, Friends, Neighbour, and Stranger.")
            return

        entry_id = save_entry_to_db(entry)

        mood_scores = {"Excited": 2, "Happy": 1, "Contented": 0, "Low": -1, "Depressed": -2}
        food_scores = {
            "Breakfast - Health balanced (Fruit & Veg)": 1,
            "Breakfast - Easy food/Snacks": -1,
            "Breakfast - I didn't have breakfast today": 0,
            "Lunch - Health balanced (Fruit & Veg)": 1,
            "Lunch - Easy food/Snacks": -1,
            "Lunch - I didn't have lunch today": 0,
            "Dinner - Health balanced (Fruit & Veg)": 1,
            "Dinner - Easy food/Snacks": -1,
            "Dinner - I didn't have dinner today": 0
        }
        water_scores = {"Adequate (>1 litre)": 1, "Low (<1 litre)": -1}
        exercise_scores = {"Gym": 1, "Cycle": 1, "Run": 1, "Walk": 1, "I didn't exercise today": -1}
        social_scores = {
            "Family - In Person": 3, "Family - By Phone": 2, "Family - By Text/Message": 1,
            "Family - I didn't socialize with family today": -1,
            "Friends - In Person": 3, "Friends - By Phone": 2, "Friends - By Text/Message": 1,
            "Friends - I didn't socialize with friends today": -1,
            "Neighbour - In Person": 3, "Neighbour - By Phone": 2, "Neighbour - By Text/Message": 1,
            "Neighbour - I didn't socialize with neighbour today": -1,
            "Stranger - In Person": 3, "Stranger - By Phone": 2, "Stranger - By Text/Message": 1,
            "Stranger - I didn't socialize with stranger today": -1
        }
        sleep_quality_scores = {"Excellent": 5, "Good": 4, "Average": 3, "Poor": 2, "Very poor": 1}
        sleep_time_scores = {"9pm": 5, "10pm": 4, "11pm": 3, "Midnight": 2, "After Midnight": 1}
        sleep_duration_scores = {
            "Less than 3 hours": 1, "3-4 hours": 2, "5-6 hours": 3, "7-8 hours": 4, "8+ hours": 5
        }

        mood_score = mood_scores.get(mood, 0)
        food_score = sum([food_scores.get(f, 0) for f in food_choices])
        water_score = water_scores.get(water, 0)
        exercise_score = exercise_scores.get(exercise, 0)
        social_score = sum([social_scores.get(s, 0) for s in social_choices])
        sleep_quality_score = sleep_quality_scores.get(sleep_quality, 0)
        sleep_time_score = sleep_time_scores.get(sleep_time, 0)
        sleep_duration_score = sleep_duration_scores.get(sleep_duration, 0)

        scores = {
            "entry_id": entry_id,
            "username": username,
            "mood_score": mood_score,
            "food_score": food_score,
            "water_score": water_score,
            "exercise_score": exercise_score,
            "social_score": social_score,
            "sleep_quality_score": sleep_quality_score,
            "sleep_time_score": sleep_time_score,
            "sleep_duration_score": sleep_duration_score
        }

        save_scores_to_db(scores)
        st.success("Entry submitted successfully!")
        st.rerun()
