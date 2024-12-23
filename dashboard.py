import streamlit as st
from garminconnect import Garmin
import pandas as pd

# Title of the Dashboard
st.title("Garmin Activity Dashboard")

# Login Section
email = st.text_input("Email", type="default", help="Enter your Garmin account email")
password = st.text_input("Password", type="password", help="Enter your Garmin account password")
login_button = st.button("Login")

if login_button:
    try:
        # Authenticate with Garmin
        client = Garmin(email, password)
        client.login()
        st.success("Login successful!")

        # Fetch recent activities
        activities = client.get_activities(0, 10)  # Fetch the latest 10 activities
        df = pd.DataFrame(activities)
        st.dataframe(df)  # Display data in a table

    except Exception as e:
        st.error(f"Failed to login: {e}")