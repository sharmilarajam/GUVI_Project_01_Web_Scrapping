# Import necessary libraries
import pymysql
import pandas as pd
import streamlit as st

# Function to create a database connection
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
    query = "SELECT `Route_Name` FROM redbus.chandigarh"

    # Fetch data
    df = fetch_data(query)

    if not df.empty:
        # Extract data as a list from a specific column
        phrases = df['Route_Name'].tolist()

        # Split and get unique towns for the "From" and "To" fields
        before_to_list = [phrase.split(" to ")[0] for phrase in phrases]
        data_list = sorted(set(before_to_list))

        # Display the list in dropdowns (selectbox)
        selected_item = st.selectbox("From", data_list)
        destination = st.selectbox("To", [city for city in data_list if city != selected_item])

        # Display the selected journey
        st.write(f'Your journey is from {selected_item} to {destination}')

        # Define the route and construct the query
        Route = selected_item + " to " + destination
        query = f"SELECT * FROM redbus.chandigarh WHERE Route_Name ='{Route}'"

        # Fetch bus data for the selected route
        bus_df = fetch_data(query)

        # Display bus information if available
        if not bus_df.empty:
            st.subheader("Available Buses")
            st.dataframe(bus_df)

            # Detailed bus information
            st.subheader("Detailed Bus Information")
            for _, row in bus_df.iterrows():
                with st.container():
                    st.write(f"### {row['Bus_Name']} - {row['Bus_Type']}")
                    st.write(f"**Departing Time:** {row['Departing_Time']}  |  **Reaching Time:** {row['Reaching_Time']}")
                    st.write(f"**Duration:** {row['Duration']}  |  **Star Rating:** {row['Star_Rating']} ⭐")
                    st.write(f"**Price:** {row['Price']}")
                    st.markdown("---")  # Separator between bus details
        else:
            st.write("No buses available for the selected route.")
        
    else:
        st.write("No route data available to display.")

if __name__ == "__main__":
    main()
