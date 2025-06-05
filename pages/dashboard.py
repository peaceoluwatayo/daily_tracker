import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from database import get_user_entries_from_db, get_user_score_from_db

# ======================= #
# ====== FUNCTIONS ====== #
# ======================= #

def render_card(title, value, color="#4CAF50"):
    st.markdown(
        f"""
        <div style="
            background-color: #f5f5f5;
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            text-align: center;
            border-left: 5px solid {color};
        ">
            <h4 style="margin: 0; color: #222; font-weight: 600;">{title}</h4>
            <h2 style="margin: 0; color: #000; font-size: 2rem;">{value}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )


def plot_category_distribution(df, column, title):
    if column in df.columns and not df[column].isnull().all():
        label_col = column.replace("_", " ").title()
        counts = df[column].value_counts().reset_index()
        counts.columns = [label_col, 'Count']
        fig = px.bar(counts, x=label_col, y='Count', color=label_col,
                     title=None,
                     color_discrete_sequence=px.colors.qualitative.Set3)
        
        fig.update_layout(
            annotations=[
                dict(
                    text=title,
                    x=0.5,
                    xref='paper',
                    y=1.15,
                    yref='paper',
                    showarrow=False,
                    font=dict(size=20, color="white"),
                    xanchor='center'
                )
            ],
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            margin=dict(t=80)
        )

        st.plotly_chart(fig, config={
            "displaylogo": False, 
            "displayModeBar": False  # This hides the entire mode bar
        })


def plot_line_chart(df, column, title, color_sequence=None):
    if column not in df.columns:
        st.warning(f"⚠️ '{column}' column not found in data.")
    elif df[column].isnull().all():
        st.info(f"ℹ️ No valid data to display for {title}.")
    else:
        chart_data = df[['entry_date', column]].dropna().sort_values('entry_date')
        chart_data['entry_date'] = chart_data['entry_date'].dt.date

        fig = px.line(
            chart_data,
            x='entry_date',
            y=column,
            markers=True,
            color_discrete_sequence=color_sequence or px.colors.qualitative.Safe
        )

        fig.update_layout(
            annotations=[
                dict(
                    text=title,
                    x=0.5,
                    xref='paper',
                    y=1.15,
                    yref='paper',
                    showarrow=False,
                    font=dict(size=20, color="white"),
                    xanchor='center'
                )
            ],
            xaxis_title="Date",
            yaxis_title=column.replace('_', ' ').title(),
            xaxis=dict(
                tickformat="%d %b %Y",
                tickangle=45,
                tickfont=dict(size=10),
                showgrid=False
            ),
            yaxis=dict(
                showgrid=False
            ),
            margin=dict(t=80)
        )

        st.plotly_chart(fig, config={
            "displaylogo": False, 
            "displayModeBar": False  # This hides the entire mode bar
        })




def plot_pie_chart(df, column, title, color_sequence=px.colors.sequential.Blues):
    if column in df.columns and not df[column].isnull().all():
        label_col = column.replace("_", " ").title()
        counts = df[column].value_counts().reset_index()
        counts.columns = [label_col, 'Count']
        fig = px.pie(
            counts,
            names=label_col,
            values='Count',
            color_discrete_sequence=color_sequence
        )

        fig.update_layout(
            annotations=[
                dict(
                    text=title,
                    x=0.5,
                    xref='paper',
                    y=1.15,
                    yref='paper',
                    showarrow=False,
                    font=dict(size=20, color="white"),
                    xanchor='center'
                )
            ],
            margin=dict(t=80)
        )

        st.plotly_chart(fig, config={
            "displaylogo": False,
            "displayModeBar": False  # This hides the entire mode bar
        })


# ======================= #
# ===== MAIN PAGE ======= #
# ======================= #

def show_dashboard():

    # Create empty columns to push the actual buttons to the right
    empty_col, col1, col2, col3 = st.columns([8, 3, 2, 2])

    with col1:
        if st.button("📋 Fill Daily Tracker Form"):
            st.session_state.page = "tracker_form"
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


    st.markdown("<h1 style='text-align: center;'>📊 Dashboard</h1>", unsafe_allow_html=True)


    # Load custom styles
    try:
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

    # Get username
    if 'username' not in st.session_state or not st.session_state['username']:
        st.session_state['username'] = st.text_input("Enter your username:")

    username = st.session_state['username']

    if username:
        with st.spinner("Loading your dashboard..."):
            user_data = get_user_entries_from_db(username)
            user_scores = get_user_score_from_db(username)

            if not user_data.empty and not user_scores.empty:
                user_data['entry_date'] = pd.to_datetime(user_data['entry_date'], errors='coerce')
                user_scores['entry_date'] = pd.to_datetime(user_scores['entry_date'], errors='coerce')

                total_entries = len(user_data)
                total_days = len(user_data['entry_date'].dt.date.unique())

                a1, a2, a3 = st.columns([1, 1, 0.5])
                with a1:
                    render_card("Total Logged Entries", total_entries)
                with a2:
                    render_card("Total Logged Days", total_days)
                with a3:
                    filter_option = st.selectbox(
                        "📅 Time Filter",
                        ("Last 7 Days", "Last 14 Days", "Last 30 Days", "All Time"),
                        index=0
                    )

                # Apply filtering
                if filter_option == "Last 7 Days":
                    start_date = datetime.now() - timedelta(days=7)
                elif filter_option == "Last 14 Days":
                    start_date = datetime.now() - timedelta(days=14)
                elif filter_option == "Last 30 Days":
                    start_date = datetime.now() - timedelta(days=30)
                else:
                    start_date = None

                if start_date:
                    filtered_data = user_data[user_data['entry_date'] >= start_date]
                    filtered_scores = user_scores[user_scores['entry_date'] >= start_date]
                else:
                    filtered_data = user_data
                    filtered_scores = user_scores

                # Categorical Bar Charts
                plot_category_distribution(filtered_data, 'mood', "🧠 Mood")
                plot_category_distribution(filtered_data, 'sleep_quality', "💤 Sleep Quality")
                plot_category_distribution(filtered_data, 'exercise', "🏃 Exercise")
                plot_category_distribution(filtered_data, 'sleep_duration', "⏱️ Sleep Duration")
                plot_category_distribution(filtered_data, 'sleep_time', "🕰️ Sleep Time")

                # Line Charts
                plot_line_chart(filtered_scores, 'food_score', '🍽️ Food Intake Over Time')
                plot_line_chart(filtered_scores, 'social_score', '🗣️ Social Interaction Over Time')

                # Pie Chart
                plot_pie_chart(filtered_data, 'water_intake', "💧 Water Intake")

            else:
                st.warning("No data found for the entered username.")
    else:
        st.info("Please enter your username to see your daily performance data.")
