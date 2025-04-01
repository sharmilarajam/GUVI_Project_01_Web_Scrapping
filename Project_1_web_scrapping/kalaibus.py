# Import necessary libraries
import pymysql
import pandas as pd
import streamlit as st
from datetime import date


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
        #st.success("Connected to the database successfully!")
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

# Streamlit app layoute
def main():
    st.set_page_config(page_title="Redbus Clone", page_icon="🚌", layout="wide")

        # Styling
    st.markdown("""
            <style>
            .main {
                background-color: #f8f9fa;
                font-family: Arial, sans-serif;
            }
            .title {
                color: #D32F2F; 
                font-size: 40px;
                font-weight: bold;
                text-align: center;
            }
            .subtitle {
                color: #757575;
                text-align: center;
            }
            .button {
                background-color: #D32F2F; 
                color: white; 
                border-radius: 5px; 
                padding: 10px 20px;
                text-align: center;
            }
            </style>
        """, unsafe_allow_html=True)

        # Title
    st.markdown("<div class='title'>Redbus</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Book Your Journey Now!</div>", unsafe_allow_html=True)

    # SQL query to fetch data
    query = "SELECT `Route_Name` FROM redbus.ap"

    # Fetch data
    df = fetch_data(query)

    if not df.empty:
        # Extract data as a list from a specific column
        phrases = df['Route_Name'].tolist()

        # Split and get unique towns for the "From" and "To" fields
        before_to_list = [phrase.split(" to ")[0] for phrase in phrases]
        data_list = sorted(set(before_to_list))

        # Display the list in dropdowns (selectbox)
        col1, col2,col3 = st.columns(3)
        with col1:
            selected_item = st.selectbox("From", data_list)
        with col2:
            destination = st.selectbox("To", [city for city in data_list if city != selected_item])

        with col3:
            # Set the minimum date to today
            min_date = date.today()
        
            # Display a date input widget with restriction to today and future dates
            selected_date = st.date_input(
                    "Select a date",
                    value=min_date,       # Default date set to today
                    min_value=min_date    # Restrict past dates
                )
        #with col4:
            #st.button("Search")    

        # Display the selected journey
        st.write(f'Your journey is from {selected_item} to {destination}')

        # Define the route and construct the query
        Route = selected_item + " to " + destination
        query = f"SELECT * FROM redbus.ap  WHERE Route_Name ='{Route}'"

        # Fetch bus data for the selected route
        bus_df = fetch_data(query)

        #counting buses
        count_buses= len(bus_df)
        st.write(f"{count_buses} Buses Available")

        # Display bus information if available
                 
        if not bus_df.empty:
            #st.subheader("Available Buses")
            st.markdown(
                "<h2 style='text-align: center; color: black;'>Available Buses</h2>",
                unsafe_allow_html=True
            )
            
            #available_columns = df[['Bus_Name', 'Bus_Type', 'Departing_Time',  'Duration', 'Reaching_Time', 'Star_Rating',  'Price', 'Seat_Availability']]
            #bus_df = df[available_columns]
            #st.dataframe(bus_df)
            # Sorting options
            st.sidebar.header("Filter Options")
            sort_by = st.sidebar.selectbox(
                "Sort by", ["Price", "Star_Rating", "Duration","Departing_Time"]
            )
            sort_order = st.sidebar.radio("Order", ["Ascending", "Descending"])

            # Apply sorting
            ascending = True if sort_order == "Ascending" else False
            sorted_bus_df = bus_df.sort_values(by=sort_by, ascending=ascending)


            

        

           # Detailed bus information
             #st.subheader("Detailed Bus Information")
            for _, row in sorted_bus_df.iterrows():
                col1, col2, col3 = st.columns([1, 2, 1])  # Adjust column width ratios for centering
                with col2:  # Center column
                 
                    st.write(f"### {row['Bus_Name']} - {row['Bus_Type']}")
                    st.write(f"**Departing Time:** {row['Departing_Time']}  |  **Reaching Time:** {row['Reaching_Time']}")
                    st.write(f"**Duration:** {row['Duration']}  |  **Star Rating:** {row['Star_Rating']} ⭐")
                    st.write(f"**Price:** {row['Price']}  |   Seat Availability:{row['Seat_Availability']}")
                    st.write(f"Link:{row['Route_Link']}")
           
                    st.markdown("---")  # Separator between bus details
        else:
            st.write("No buses available for the selected route.")
        
    else:
        st.write("No route data available to display.")

if __name__ == "__main__":
    main()
