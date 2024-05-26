import streamlit as st
import pandas as pd
import datetime as dt

# Function to save DataFrame
def save_dataframe(df):
    df.to_csv("daily_log.csv", index=False)  # Saves to a CSV file

# Function to load DataFrame (if it exists)
def load_dataframe():
    try:
        df = pd.read_csv("daily_log.csv")
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

    # Navigation
    menu = ["Home", "View Raw Logs", "View Logs", "View Charts"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
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
    elif choice == "View Raw Logs":
        st.subheader("View LogEntries")
        # Display DataFrame with sorting and filtering options
        st.dataframe(st.session_state.df)
    elif choice == "View Logs":
        st.subheader("View LogEntries")
        temp = st.session_state.df
        print(temp)
        # Add filters for tags and dates
        tags = st.multiselect("Select tags", st.session_state.df['Tags'].unique())

        date = st.date_input("Select date", dt.datetime.now())
        date = pd.to_datetime(date)
        if tags:
            temp = temp[temp['Tags'].isin(tags)]
        if not st.checkbox("Show all logs", True):
            if date:
                #temp['Date'] = pd.to_datetime(temp['Date'])
                temp = temp[temp['Date'].date() == date.date()]

        # Display DataFrame with sorting and filtering options
        for i, row in temp.iterrows():
            with st.container(border=True):
                st.write(f"LogEntry: {row['LogEntry']}")
                st.write(f"Tags: {row['Tags']}")
                st.write(f"Date: {row['Date']}")
    elif choice == "View Charts":
        st.subheader("View LogEntries")
        temp = st.session_state.df

        # Add a chart for the number of logs per day
        temp['Date'] = pd.to_datetime(temp['Date']).dt.date
        st.line_chart(temp['Date'].value_counts())

        

if __name__ == "__main__":
    main()