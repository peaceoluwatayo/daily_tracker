# # Options under questions
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
#     mood = st.selectbox("mood", ["Choose an option", "Excited", "Happy", "Contented", "Low", "Depressed"] , label_visibility="collapsed")
#     close_div()

#     styled_question("2. What did you eat today? (Select all that apply)")
#     food_choices = st.multiselect("food_choices", [
#         "Breakfast - Health balanced (Fruit & Veg)",
#         "Breakfast - Easy food/Snacks",
#         "Breakfast - I didn't have breakfast today",
#         "Lunch - Health balanced (Fruit & Veg)",
#         "Lunch - Easy food/Snacks",
#         "Lunch - I didn't have lunch today",
#         "Dinner - Health balanced (Fruit & Veg)",
#         "Dinner - Easy food/Snacks",
#         "Dinner - I didn't have dinner today"
#     ], label_visibility="collapsed")
#     close_div()

#     styled_question("3. How was your water intake today?")
#     water = st.selectbox("water", ["Choose an option", "Adequate (>1 litre)", "Low (<1 litre)"], label_visibility="collapsed" )
#     close_div()

#     styled_question("4. Did you exercise today?")
#     exercise = st.selectbox("exercise", ["Choose an option", "Gym", "Cycle", "Run", "Walk", "I didn't exercise today"], label_visibility="collapsed")
#     close_div()

#     styled_question("5. Did you socialise today? (Select all that apply)")
#     social_choices = st.multiselect("social_choices", [
#         "Family - In Person", "Family - By Phone", "Family - By Text/Message", "Family - I didn't socialize with family today",
#         "Friends - In Person", "Friends - By Phone", "Friends - By Text/Message", "Friends - I didn't socialize with friends today",
#         "Neighbour - In Person", "Neighbour - By Phone", "Neighbour - By Text/Message", "Neighbour - I didn't socialize with neighbour today",
#         "Stranger - In Person", "Stranger - By Phone", "Stranger - By Text/Message", "Stranger - I didn't socialize with stranger today"
#     ], label_visibility="collapsed")
#     close_div()

#     styled_question("6. How was your sleep last night?")
#     sleep_quality = st.selectbox("sleep_quality", ["Choose an option", "Excellent", "Good", "Average", "Poor", "Very poor"], label_visibility="collapsed")
#     close_div()

#     styled_question("7. What time did you go to sleep last night?")
#     sleep_time = st.selectbox("sleep_time", ["Choose an option", "9pm", "10pm", "11pm", "Midnight", "After Midnight"], label_visibility="collapsed")
#     close_div()

#     styled_question("8. How many hours of sleep did you get last night?")
#     sleep_duration = st.selectbox("sleep_duration", ["Choose an option", "Less than 3 hours", "3-4 hours", "5-6 hours", "7-8 hours", "8+ hours"], label_visibility="collapsed")
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





# # Options beside questions
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

#     def render_question(question, widget_type="selectbox", options=None):
#         # Increase the font size for the question and set a smaller font for the options
#         col1, col2 = st.columns([3.5, 4.5])
#         with col1:
#             st.markdown(f"<span style='font-size:20px; font-weight:bold;'>{question}</span>", unsafe_allow_html=True)
#         with col2:
#             if widget_type == "selectbox":
#                 return st.selectbox(" ", options, label_visibility="collapsed", key=question)
#             elif widget_type == "multiselect":
#                 return st.multiselect(" ", options, label_visibility="collapsed", key=question)

#     # ---------- FORM QUESTIONS ----------
#     mood = render_question("1. How are you feeling today?", "selectbox", 
#         ["Choose an option", "Excited", "Happy", "Contented", "Low", "Depressed"])

#     food_choices = render_question("2. What did you eat today? (Select all that apply)", "multiselect", [
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

#     water = render_question("3. How was your water intake today?", "selectbox",
#         ["Choose an option", "Adequate (>1 litre)", "Low (<1 litre)"])

#     exercise = render_question("4. Did you exercise today?", "selectbox",
#         ["Choose an option", "Gym", "Cycle", "Run", "Walk", "I didn't exercise today"])

#     social_choices = render_question("5. Did you socialise today? (Select all that apply)", "multiselect", [
#         "Family - In Person", "Family - By Phone", "Family - By Text/Message", "Family - I didn't socialize with family today",
#         "Friends - In Person", "Friends - By Phone", "Friends - By Text/Message", "Friends - I didn't socialize with friends today",
#         "Neighbour - In Person", "Neighbour - By Phone", "Neighbour - By Text/Message", "Neighbour - I didn't socialize with neighbour today",
#         "Stranger - In Person", "Stranger - By Phone", "Stranger - By Text/Message", "Stranger - I didn't socialize with stranger today"
#     ])

#     sleep_quality = render_question("6. How was your sleep last night?", "selectbox",
#         ["Choose an option", "Excellent", "Good", "Average", "Poor", "Very poor"])

#     sleep_time = render_question("7. What time did you go to sleep last night?", "selectbox",
#         ["Choose an option", "9pm", "10pm", "11pm", "Midnight", "After Midnight"])

#     sleep_duration = render_question("8. How many hours of sleep did you get last night?", "selectbox",
#         ["Choose an option", "Less than 3 hours", "3-4 hours", "5-6 hours", "7-8 hours", "8+ hours"])

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



# Typeform like
import streamlit as st
from database import save_entry_to_db, save_scores_to_db, has_filled_form_today

def show_tracker_form():
    
    # Create empty columns to push the actual buttons to the right
    empty_col, col1, col2, col3 = st.columns([8, 3, 2, 2])

    with col1:
        if st.button("📊 View Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()

    with col2:
        if st.button("📜 View History"):
            st.session_state.page = "history"
            st.rerun()

    with col3:
        if st.button("Logout"):
            st.session_state.clear()
            st.session_state.page = "login"
            st.rerun()


    st.markdown("<h1 style='text-align: center;'>📝 Daily Tracker Form</h1>", unsafe_allow_html=True)

    username = st.session_state.get("username")
    if has_filled_form_today(username):
        st.warning("You have already submitted your form for today!")
        return

    if "form_step" not in st.session_state:
        st.session_state.form_step = 1
    if "answers" not in st.session_state:
        st.session_state.answers = {}

    total_steps = 8
    progress = (st.session_state.form_step - 1) / total_steps

    step = st.session_state.form_step

    def styled_question(question_text):
        st.markdown(f"<div style='font-size:22px; font-weight:bold;'>{question_text}</div>", unsafe_allow_html=True)

    def next_step():
        if st.session_state.form_step < total_steps:
            st.session_state.form_step += 1

    def previous_step():
        if st.session_state.form_step > 1:
            st.session_state.form_step -= 1

    answers = st.session_state.answers

    # Question Form
    if step == 1:
        styled_question("1. How are you feeling today?")
        mood = st.selectbox(
            "Mood",
            ["Choose an option", "Excited", "Happy", "Contented", "Low", "Depressed"],
            index=["Choose an option", "Excited", "Happy", "Contented", "Low", "Depressed"].index(answers.get("mood", "Choose an option")),
            label_visibility="collapsed"
        )
        if mood != "Choose an option":
            answers["mood"] = mood
            st.button("Next", on_click=next_step)

    elif step == 2:
        styled_question("2. What did you eat today? (Select all that apply)")
        food_choices = st.multiselect(
            "Food Choices",
            options=[
                "Breakfast - Health balanced (Fruit & Veg)",
                "Breakfast - Easy food/Snacks",
                "Breakfast - I didn't have breakfast today",
                "Lunch - Health balanced (Fruit & Veg)",
                "Lunch - Easy food/Snacks",
                "Lunch - I didn't have lunch today",
                "Dinner - Health balanced (Fruit & Veg)",
                "Dinner - Easy food/Snacks",
                "Dinner - I didn't have dinner today"
            ],
            default=answers.get("food_choices", []),
            label_visibility="collapsed"
        )
        if food_choices:
            has_breakfast = any("Breakfast" in f for f in food_choices)
            has_lunch = any("Lunch" in f for f in food_choices)
            has_dinner = any("Dinner" in f for f in food_choices)

            if has_breakfast and has_lunch and has_dinner:
                answers["food_choices"] = food_choices
                st.button("Next", on_click=next_step)
            else:
                st.warning("Please select at least one option for Breakfast, Lunch, and Dinner.")

    elif step == 3:
        styled_question("3. How was your water intake today?")
        water = st.selectbox(
            "Water Intake",
            ["Choose an option", "Adequate (>1 litre)", "Low (<1 litre)"],
            index=["Choose an option", "Adequate (>1 litre)", "Low (<1 litre)"].index(answers.get("water", "Choose an option")),
            label_visibility="collapsed"
        )
        if water != "Choose an option":
            answers["water"] = water
            st.button("Next", on_click=next_step)

    elif step == 4:
        styled_question("4. Did you exercise today?")
        exercise = st.selectbox(
            "Exercise",
            ["Choose an option", "Gym", "Cycle", "Run", "Walk", "I didn't exercise today"],
            index=["Choose an option", "Gym", "Cycle", "Run", "Walk", "I didn't exercise today"].index(answers.get("exercise", "Choose an option")),
            label_visibility="collapsed"
        )
        if exercise != "Choose an option":
            answers["exercise"] = exercise
            st.button("Next", on_click=next_step)

    elif step == 5:
        styled_question("5. Did you socialise today? (Select all that apply)")
        social_choices = st.multiselect(
            "Social Choices",
            options=[
                "Family - In Person", "Family - By Phone", "Family - By Text/Message", "Family - I didn't socialize with family today",
                "Friends - In Person", "Friends - By Phone", "Friends - By Text/Message", "Friends - I didn't socialize with friends today",
                "Neighbour - In Person", "Neighbour - By Phone", "Neighbour - By Text/Message", "Neighbour - I didn't socialize with neighbour today",
                "Stranger - In Person", "Stranger - By Phone", "Stranger - By Text/Message", "Stranger - I didn't socialize with stranger today"
            ],
            default=answers.get("social_choices", []),
            label_visibility="collapsed"
        )
        if social_choices:
            has_family = any("Family" in s for s in social_choices)
            has_friends = any("Friends" in s for s in social_choices)
            has_neighbour = any("Neighbour" in s for s in social_choices)
            has_stranger = any("Stranger" in s for s in social_choices)

            if has_family and has_friends and has_neighbour and has_stranger:
                answers["social_choices"] = social_choices
                st.button("Next", on_click=next_step)
            else:
                st.warning("Please select at least one option for Family, Friends, Neighbour, and Stranger.")

    elif step == 6:
        styled_question("6. How was your sleep last night?")
        sleep_quality = st.selectbox(
            "Sleep Quality",
            ["Choose an option", "Excellent", "Good", "Average", "Poor", "Very poor"],
            index=["Choose an option", "Excellent", "Good", "Average", "Poor", "Very poor"].index(answers.get("sleep_quality", "Choose an option")),
            label_visibility="collapsed"
        )
        if sleep_quality != "Choose an option":
            answers["sleep_quality"] = sleep_quality
            st.button("Next", on_click=next_step)

    elif step == 7:
        styled_question("7. What time did you go to sleep last night?")
        sleep_time = st.selectbox(
            "Sleep Time",
            ["Choose an option", "9pm", "10pm", "11pm", "Midnight", "After Midnight"],
            index=["Choose an option", "9pm", "10pm", "11pm", "Midnight", "After Midnight"].index(answers.get("sleep_time", "Choose an option")),
            label_visibility="collapsed"
        )
        if sleep_time != "Choose an option":
            answers["sleep_time"] = sleep_time
            st.button("Next", on_click=next_step)

    elif step == 8:
        styled_question("8. How many hours of sleep did you get last night?")
        sleep_duration = st.selectbox(
            "Sleep Duration",
            ["Choose an option", "Less than 3 hours", "3-4 hours", "5-6 hours", "7-8 hours", "8+ hours"],
            index=["Choose an option", "Less than 3 hours", "3-4 hours", "5-6 hours", "7-8 hours", "8+ hours"].index(answers.get("sleep_duration", "Choose an option")),
            label_visibility="collapsed"
        )
        if sleep_duration != "Choose an option":
            answers["sleep_duration"] = sleep_duration
            if st.button("Submit Entry"):
                submit_entry(username)

    st.progress(progress)

    if step > 1:
        st.button("Previous", on_click=previous_step)

def submit_entry(username):
    answers = st.session_state.answers
    food_choices = answers["food_choices"]
    social_choices = answers["social_choices"]

    entry = {
        "username": username,
        "mood": answers["mood"],
        "food": ", ".join(food_choices),
        "water": answers["water"],
        "exercise": answers["exercise"],
        "social": ", ".join(social_choices),
        "sleep_quality": answers["sleep_quality"],
        "sleep_time": answers["sleep_time"],
        "sleep_duration": answers["sleep_duration"]
    }

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
        "Family - In Person": 3, "Family - By Phone": 2, "Family - By Text/Message": 1, "Family - I didn't socialize with family today": -1,
        "Friends - In Person": 3, "Friends - By Phone": 2, "Friends - By Text/Message": 1, "Friends - I didn't socialize with friends today": -1,
        "Neighbour - In Person": 3, "Neighbour - By Phone": 2, "Neighbour - By Text/Message": 1, "Neighbour - I didn't socialize with neighbour today": -1,
        "Stranger - In Person": 3, "Stranger - By Phone": 2, "Stranger - By Text/Message": 1, "Stranger - I didn't socialize with stranger today": -1
    }
    sleep_quality_scores = {"Excellent": 5, "Good": 4, "Average": 3, "Poor": 2, "Very poor": 1}
    sleep_time_scores = {"9pm": 5, "10pm": 4, "11pm": 3, "Midnight": 2, "After Midnight": 1}
    sleep_duration_scores = {"Less than 3 hours": 1, "3-4 hours": 2, "5-6 hours": 3, "7-8 hours": 4, "8+ hours": 5}

    scores = {
        "entry_id": entry_id,
        "username": username,
        "mood_score": mood_scores.get(answers["mood"], 0),
        "food_score": sum([food_scores.get(f, 0) for f in food_choices]),
        "water_score": water_scores.get(answers["water"], 0),
        "exercise_score": exercise_scores.get(answers["exercise"], 0),
        "social_score": sum([social_scores.get(s, 0) for s in social_choices]),
        "sleep_quality_score": sleep_quality_scores.get(answers["sleep_quality"], 0),
        "sleep_time_score": sleep_time_scores.get(answers["sleep_time"], 0),
        "sleep_duration_score": sleep_duration_scores.get(answers["sleep_duration"], 0),
    }

    save_scores_to_db(scores)
    st.success("Entry submitted successfully!")
    st.session_state.form_step = 1
    st.session_state.answers = {}
    st.rerun()
