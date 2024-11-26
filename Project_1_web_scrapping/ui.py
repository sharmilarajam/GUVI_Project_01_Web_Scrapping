# Function to connect to the database
import pymysql
import pandas as pd
import streamlit as st


def create_connection():
    connection = None
    try:
        connection = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="123456",
            database="redbus"
        )
        st.success("Connected to the database successfully!")
    except pymysql.MySQLError as e:
        st.error(f"Error: {e}")
    return connection


# Fetch data from the database
def fetch_data(query):
    connection = create_connection()
    if connection is None:
        return pd.DataFrame()  # Return an empty DataFrame if the connection failed

    try:
        # Using pandas to fetch data directly into a DataFrame
        df = pd.read_sql(query, connection)
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()
    finally:
        connection.close()

# Streamlit app layout
def main():
    st.title("KalaiBus")

    # SQL query to fetch data
    query = "SELECT `Route_Name` FROM redbus.chandigarh" # Replace with your actual column and table name

    # Fetch data
    df = fetch_data(query)

    if not df.empty:
        # Extract data as a list from a specific column
        phrases = df['Route_Name'].tolist()  # Replace with your column name 

        #to split route into single town
        before_to_list = [phrase.split(" to ")[0] for phrase in phrases]
        data_list=set(before_to_list)


        # Display the list in a listbox (selectbox)
        selected_item = st.selectbox("From ", data_list)
        destination = st.selectbox("To", data_list)

        # Display the selected item
        st.write(f' your journey is start from {selected_item }  to  { destination}')
    else:
        st.write("No data available to display.")

if __name__ == "__main__":
    main()
