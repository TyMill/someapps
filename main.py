
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="My Calendar App", page_icon=":calendar:", layout="wide")

# load dataframe
df = pd.read_csv("some_sth.csv")

# define threshold values
thresholds = {0.2: 0.95, 0.4: 0.98, 0.6: 1.03, 0.8: 1.076}

# define multipliers based on time range
multipliers = {"8:00am": 1.05, "8:30am": 1.04, "9:00am": 1.03, "9:30am": 1.02, "10:00am": 1.01, "10:30am": 1, "11:00am": 1, "11:30am": 1, "12:00pm": 1.01, "12:30pm": 1.02, "1:00pm": 1.03, "1:30pm": 1.04, "2:00pm": 1.05, "2:30pm": 1.06, "3:00pm": 1.07, "3:30pm": 1.08, "4:00pm": 1.09, "4:30pm": 1.1, "5:00pm": 1.1}

# create calendar
st.set_page_config(page_title="Day Planner", page_icon=":calendar:", layout="wide")
calendar_value = st.date_input("Select a date", value=datetime.now())

if calendar_value:
    # create time range picker
    start_time = datetime.strptime(st.time_input("Select start time (8am to 5pm)", datetime.strptime("08:00", "%H:%M").time()).strftime("%H:%M"), "%H:%M")
    end_time = datetime.strptime(st.time_input("Select end time (8am to 5pm)", datetime.strptime("17:00", "%H:%M").time()).strftime("%H:%M"), "%H:%M")
    current_time = start_time
    values = []
    while current_time <= end_time:
        values.append(st.checkbox(current_time.strftime("%I:%M %p")))
        current_time += timedelta(minutes=30)
    selected_times = [current_time.strftime("%I:%M %p") for current_time, value in zip(time_range, values) if value]

# filter dataframe by date and time range
df_filtered = df[(df["date"] == calendar_value.strftime("%Y-%m-%d")) & (df["time"].isin([time.strftime("%H:%M") for time in values]))]

# check if Not aval percentage is greater than a threshold
if df_filtered['Not aval'].sum()/df_filtered.shape[0] > threshold:
    st.warning("The percentage of 'Not aval' for the selected date is greater than the threshold.")
    for threshold, multiplier in thresholds.items():
        if df_filtered['Not aval'].sum()/df_filtered.shape[0] > threshold:
            df_filtered.loc[:, 'value'] = df_filtered['value'] * multiplier
            break
else:
    st.dataframe(df_filtered)

# apply multipliers based on time range
for time, multiplier in multipliers.items():
    if time in values:
        df_filtered.loc[df_filtered["time"] == time, "value"] = df_filtered.loc[df_filtered["time"] == time, "value"] * multiplier

# display dataframe
st.dataframe(df_filtered)
