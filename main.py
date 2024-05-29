import streamlit as st
import pandas as pd
import datetime as dt

LOG_FILE = "daily_log.csv"

def save_dataframe(df):
    df.to_csv(LOG_FILE, index=False)  # Saves to a CSV file

def load_dataframe():
    try:
        return pd.read_csv(LOG_FILE)
    except FileNotFoundError:
        # Create an empty DataFrame if file not found
        return pd.DataFrame(columns=['LogEntry', 'Tags', 'Date'])

def submit_entry():
    st.session_state.new_entry = st.session_state.entry_textarea
    st.session_state.entry_textarea = ''

def main():
    st.title("Captain's Log")
    st.logo('father.jpg')
    if 'df' not in st.session_state:
        st.session_state.df = load_dataframe()
    if "tags" not in st.session_state:
            st.session_state.tags = ['Log', 'AE Standup', 'RO Standup', 'Task', 'Reminder']
    
    ADD = "Add Log Entry"
    LOGS_RAW = "View Raw Logs"
    LOGS = "View Logs"
    CHARTS = "View Charts"

    navigation_views = [ADD, LOGS_RAW, LOGS, CHARTS]
    navigation_choice = st.sidebar.selectbox("Menu", navigation_views)

    if navigation_choice == ADD:
        st.subheader("Add a new Log. . .")
        date = st.date_input("Select date", dt.datetime.now(), key="date_input")
        
        # Input for new LogEntry
        if "entry_textarea" not in st.session_state:
            st.session_state.entry_textarea = ""
        if "new_entry" not in st.session_state:
            st.session_state.new_entry = ""

        st.text_area('Entry', height=20, label_visibility="collapsed", key="entry_textarea")
        st.write(f"You wrote {len(st.session_state.new_entry)} characters.")
        selected_tags = st.multiselect("Select tags", st.session_state.tags, default='Log', key="tags_multiselect")

        if st.button("Add", key="add_button", on_click=submit_entry):
            st.session_state.df.loc[len(st.session_state.df)] = pd.Series(
                {'LogEntry': "\n".join(st.session_state.new_entry.splitlines()), 
                'Tags': ", ".join(selected_tags), 
                'Date': pd.to_datetime(date)})
            save_dataframe(st.session_state.df)  

    elif navigation_choice == LOGS_RAW:
        st.subheader(LOGS_RAW)
        st.dataframe(st.session_state.df)

    elif navigation_choice == LOGS:
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

        temp = temp.iloc[::-1] # Reverse the order of logs
        for i, row in temp.iterrows():
            with st.container(border=True):
                st.write(f"Log Entry: {row['LogEntry']}")
                st.write(f"Tags: {row['Tags']}")
                st.write(f"Date: {row['Date']}")

    elif navigation_choice == CHARTS:
        st.subheader(CHARTS)
        temp = st.session_state.df
        temp['Date'] = pd.to_datetime(temp['Date']).dt.date
        st.line_chart(temp['Date'].value_counts()) # Line chart of log entries by date
        
        temp['LogLength'] = temp['LogEntry'].apply(len)
        st.line_chart(temp.groupby('Date')['LogLength'].mean()) # Chart of log length by date

if __name__ == "__main__":
    main()