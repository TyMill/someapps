import pandas as pd
import streamlit as st

# Create sample data frame
df = pd.DataFrame({'Date': ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04'],
                   'Place': ['NY', 'LA', 'SF', 'NY'],
                   'Value': [10, 20, 30, 40]})
df['Date'] = pd.to_datetime(df['Date'])

def filter_by_date_place(df, date, place):
    return df[(df['Date'] == date) & (df['Place'] == place)]

def main():
    st.title("Calendar and Data")
    date = st.date_input("Select Date", value=df['Date'].min())
    place = st.selectbox("Select Place", df['Place'].unique())
    filtered_df = filter_by_date_place(df, date, place)
    st.write("Data for selected date and place:")
    st.write(filtered_df)

if __name__ == '__main__':
    main()
