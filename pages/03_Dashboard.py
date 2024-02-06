import streamlit as st
import pandas as pd
import datetime

st.set_page_config(layout="centered", page_icon="🥰📊", page_title="MoodTune Dashboard")
st.markdown('# :blue[MoodTune] Dashboard 🥰')
st.markdown("""
        <style>
        html, body, [class*="css"]  {
            font-weight:600;
		}
        h1{
            text-align: center;
        }
        [data-testid=stSidebar] {
            background-color: #ADD8E6;
        }
        </style>
        """, unsafe_allow_html=True)

# Load your DataFrame from the CSV file
df = pd.read_csv('journal_entries.csv', delimiter=',')

# Function to filter entries based on the selected date interval
def filter_entries(start_date, end_date):
    # Convert 'Date' column to datetime with errors='coerce'
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Filter out rows with NaT values (invalid datetime strings)
    valid_date_df = df.dropna(subset=['Date'])

    # Filter entries based on valid date values and date range
    filtered_df = valid_date_df[
        (valid_date_df['Date'] >= pd.Timestamp(start_date)) & (valid_date_df['Date'] <= pd.Timestamp(end_date))
    ]

    return filtered_df

# Select date interval using st.date_input
today = datetime.datetime.now()
this_year = today.year
jan_1 = datetime.date(this_year, 1, 1)
dec_31 = datetime.date(this_year, 12, 31)

# Select date interval using st.date_input
selected_date_range = st.sidebar.date_input(
    "Select date interval",
    (jan_1, dec_31),
    jan_1,
    dec_31,
    format="YYYY/MM/DD",
)

start_date, end_date = selected_date_range
start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)
filtered_entries = filter_entries(start_date, end_date)
filtered_entries['Date'] = filtered_entries['Date'].dt.date

try:
    # Check if the start date is after the end date
    if start_date > end_date:
        st.markdown("**Incorrect date interval entered. Start date cannot be after end date.**", unsafe_allow_html=True)
    else:
        filtered_entries = filter_entries(start_date, end_date)
        filtered_entries['Date'] = filtered_entries['Date'].dt.date

        # Display entries if found
        if not filtered_entries.empty:
            # Iterate over DataFrame rows only once
            for index, row in filtered_entries.iterrows():
                # Access each column value
                column1 = row["Date"]
                column2 = row['Emotion']
                column3 = row['Reason for emotion']

                # Create a box for each row
                with st.container(height=150, border=True):
                    st.markdown(f"##### **:blue[{column1}]**")
                    st.markdown(f"**Emotion:** {column2}")
                    st.markdown(f"**What happened:** {column3}")

        else:
            st.markdown("**No entries found for the selected date range.**", unsafe_allow_html=True)

except Exception as e:
    # Handle any other exceptions
    st.markdown(f"**Error:** {str(e)}", unsafe_allow_html=True)