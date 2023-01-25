
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


# load dataframe
df = pd.read_csv("some_sth.csv",sep=";")

# define threshold values
thresholds = {0.2: 0.95, 0.4: 0.98, 0.6: 1.03, 0.8: 1.076}

# define multipliers based on time range
multipliers = {"8:00": 1.05, "8:30": 1.04, "9:00": 1.03, "9:30": 1.02, "10:00": 1.01, "10:30": 1, "11:00": 1, "11:30": 1, "12:00": 1.01, "12:30": 1.02, "13:00": 1.03, "13:30": 1.04, "14:00": 1.05, "14:30": 1.06, "15:00": 1.07, "15:30": 1.08, "16:00pm": 1.09, "16:30": 1.1, "17:00": 1.1}

time_range = ["8:00", "8:30", "9:00", "9:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00"]
# create calendar
st.set_page_config(page_title="Day Planner", page_icon=":calendar:", layout="wide")
calendar_value = st.date_input("Select a date", value=datetime.now())

if calendar_value:
    # create time range picker
    start_time = datetime.strptime(st.time_input("Select start time (8 to 17)", datetime.strptime("08:00", "%H:%M").time()).strftime("%H:%M"), "%H:%M")
    end_time = datetime.strptime(st.time_input("Select end time (8 to 117)", datetime.strptime("17:00", "%H:%M").time()).strftime("%H:%M"), "%H:%M")
    current_time = start_time
    values = []
    while current_time <= end_time:
        values.append(st.checkbox(current_time.strftime("%I:%M %p")))
        current_time += timedelta(minutes=30)
    selected_times = [current_time.strftime("%I:%M %p") for current_time, value in zip(time_range, values) if value]

# filter dataframe by date and time range
df_filtered = df[(df["date"] == calendar_value.strftime("%Y-%m-%d")) & (df["time"].isin([time.strftime("%H:%M") for time in values]))]
st.dataframe(df_filtered)
# check if Not aval percentage is greater than a threshold
if df_filtered['not aval'].sum()/df_filtered.shape[0] > threshold:
    st.warning("The percentage of 'Not aval' for the selected date is greater than the threshold.")
    for threshold, multiplier in thresholds.items():
        if df_filtered['not aval'].sum()/df_filtered.shape[0] > threshold:
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
