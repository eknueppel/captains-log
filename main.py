import streamlit as st
import pandas as pd
import datetime as dt

LOG_FILE = "daily_log.csv"

# Function to save DataFrame
def save_dataframe(df):
    df.to_csv(LOG_FILE, index=False)  # Saves to a CSV file

# Function to load DataFrame (if it exists)
def load_dataframe():
    try:
        df = pd.read_csv(LOG_FILE)
        return df
    except FileNotFoundError:
        # Create an empty DataFrame if file not found
        return pd.DataFrame(columns=['LogEntry', 'Tags', 'Date', 'Time'])

# Main app
def main():
    # Initialize an empty DataFrame
    if 'df' not in st.session_state:
        st.session_state.df = load_dataframe()

    st.title("Captain's Log")
    st.logo('father.jpg')
    # View Constants
    ADD = "Add Log Entry"
    LOGS_RAW = "View Raw Logs"
    LOGS = "View Logs"
    CHARTS = "View Charts"

    # Navigation
    views = [ADD, LOGS_RAW, LOGS, CHARTS]
    choice = st.sidebar.selectbox("Menu", views)

    if choice == ADD:
        st.subheader("Add a new Log. . .")
        date = st.date_input("Select date", dt.datetime.now(), key="date_input")
        # Input for new LogEntry
        new_entry = st.text_area('Entry', height=20, label_visibility="collapsed", key="entry_textarea")
        st.write(f"You wrote {len(new_entry)} characters.")
        # Multiselect for tag selection
        tags = ['Log', 'AE Standup', 'RO Standup', 'Task', 'Reminder']
        selected_tags = st.multiselect("Select tags", tags, default='Log', key="tags_multiselect")

        if st.button("Add", key="add_button"):
            st.session_state.df.loc[len(st.session_state.df)] = pd.Series(
                {'LogEntry': "\n".join(new_entry.splitlines()), 
                'Tags': ", ".join(selected_tags), 
                'Date': pd.to_datetime(date)})
            # Save the updated DataFrame
            save_dataframe(st.session_state.df)  
              
    elif choice == LOGS_RAW:
        st.subheader(LOGS_RAW)
        # Display DataFrame with sorting and filtering options
        st.dataframe(st.session_state.df)

    elif choice == LOGS:
        st.subheader(LOGS)
        temp = st.session_state.df
        temp['Date'] = pd.to_datetime(temp['Date'])

        # Add filters for tags and dates
        tags = st.multiselect("Select tags", st.session_state.df['Tags'].unique())
        date = st.date_input("Select date", dt.datetime.now())
        
        if tags:
            temp = temp[temp['Tags'].isin(tags)]
        if not st.checkbox("Show all logs", True):
            if date:
                temp = temp[temp['Date'] == pd.to_datetime(date)]

        # Display DataFrame with sorting and filtering options
        for i, row in temp.iterrows():
            with st.container(border=True):
                st.write(f"LogEntry: {row['LogEntry']}")
                st.write(f"Tags: {row['Tags']}")
                st.write(f"Date: {row['Date']}")

    elif choice == CHARTS:
        st.subheader(CHARTS)
        temp = st.session_state.df

        # Add a chart for the number of logs per day
        temp['Date'] = pd.to_datetime(temp['Date']).dt.date
        st.line_chart(temp['Date'].value_counts())

        

if __name__ == "__main__":
    main()