import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from garminconnect import Garmin

# Streamlit app title
st.title("Garmin End-of-Year Dashboard")

# User authentication
try:
    # Assuming you've already set up login
    email = st.secrets["GARMIN_EMAIL"]
    password = st.secrets["GARMIN_PASSWORD"]

    # Login to Garmin
    client = Garmin(email, password)
    client.login()
    st.success("Logged in successfully!")
except Exception as e:
    st.error("Error logging in. Please check your credentials.")
    st.stop()

# Fetch step data
def get_step_data(days=7):
    today = datetime.now()
    dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days)]
    step_data = []

    for date in dates:
        try:
            daily_data = client.get_steps_data(date)
            steps = daily_data[0]['steps'] if daily_data else 0
            goal = daily_data[0]['goal'] if daily_data else 0
            step_data.append({"date": date, "steps": steps, "goal": goal})
        except Exception as e:
            step_data.append({"date": date, "steps": 0, "goal": 0})

    return pd.DataFrame(step_data)

# Get data for the past 7 days
step_data = get_step_data(7)

# Calculate streak
step_data['goal_met'] = step_data['steps'] >= step_data['goal']
step_data['streak'] = step_data['goal_met'].cumsum()

# Display step goal data
st.header("Step Goals Overview")

# Bar chart for steps vs. goal
st.bar_chart(step_data[['steps', 'goal']].set_index(step_data['date']))

# Display streak information
current_streak = (step_data['goal_met'][::-1].cumprod().sum())
st.metric("Current Streak (days)", current_streak)

# Additional stats
total_steps = step_data['steps'].sum()
days_goal_met = step_data['goal_met'].sum()
st.write(f"**Total Steps (Last 7 Days):** {total_steps}")
st.write(f"**Days Goals Met (Last 7 Days):** {days_goal_met} / {len(step_data)}")

# Debug output (optional)
if st.checkbox("Show raw data"):
    st.write(step_data)