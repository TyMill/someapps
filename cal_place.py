import pandas as pd
import streamlit as st

# Create sample data frame
df = pd.DataFrame({'Date': ['2022-01-01', '2022-01-01', '2022-01-02', '2022-01-02'],
                   'Hour': [8, 12, 8, 12],
                   'Place': ['A', 'A', 'B', 'B'],
                   'Value': [10, 20, 30, 40]})
df['Date'] = pd.to_datetime(df['Date'])

def filter_by_date_hour_place(df, date, hour, place):
    return df[(df['Date'] == date) & (df['Hour'] == hour) & (df['Place'] == place)]

def main():
    st.title("Calendar and Data")
    date = st.date_input("Select Date", value=df['Date'].min())
    hour = st.selectbox("Select Hour", [8, 12])
    place = st.selectbox("Select Place", ['A', 'B'])
    filtered_df = filter_by_date_hour_place(df, date, hour, place)
    st.write("Data for selected date, hour, and place:")
    st.write(filtered_df)

if __name__ == '__main__':
    main()
