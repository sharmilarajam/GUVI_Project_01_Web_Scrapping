import pymysql
import pandas as pd
import streamlit as st
from datetime import date
import base64

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
    except pymysql.MySQLError as e:
        st.error(f"Error: {e}")
    return connection

# Fetch data from the database
def fetch_data(query):
    connection = create_connection()
    if connection is None:
        return pd.DataFrame()
    try:
        df = pd.read_sql(query, connection)
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()
    finally:
        connection.close()

# Function to set background from URL


# Function to set background image
def set_bg_from_url(url):
    css = f"""
    <style>
    .stApp {{
        background-image: url("{url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        height: 100vh;  /* Ensure background covers full screen */
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Main Streamlit app layout
def main():
    st.set_page_config(page_title="Redbus Clone", page_icon="🚌", layout="wide")
    
    #set_bg_from_url("https://media.istockphoto.com/id/1616050163/photo/white-intercity-bus-in-the-parking-lot.webp?a=1&b=1&s=612x612&w=0&k=20&c=AGq5boBnk-6GNfDfbF_D0SAfMJfxECxOaZGgfvRpOxg=")
    
    # Styling
    st.markdown("""
        <style>
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
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='title'>Redbus</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Book Your Journey Now!</div>", unsafe_allow_html=True)

    # SQL query to fetch data
    query = "SELECT `Route_Name` FROM redbus.ap"
    df = fetch_data(query)

    if not df.empty:
        phrases = df['Route_Name'].tolist()
        before_to_list = [phrase.split(" to ")[0] for phrase in phrases]
        data_list = sorted(set(before_to_list))

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<h5 style='font-weight:bold;'>From</h5>", unsafe_allow_html=True)
            selected_item = st.selectbox("", data_list)

        with col2:
            st.markdown("<h5 style='font-weight:bold;'>To</h5>", unsafe_allow_html=True)
            destination = st.selectbox("", [city for city in data_list if city != selected_item])

        with col3:
            st.markdown("<h5 style='font-weight:bold;'>Select a date</h5>", unsafe_allow_html=True)
            selected_date = st.date_input("", value=date.today(), min_value=date.today())

        st.markdown(f"**Your journey is from {selected_item} to {destination}**")


        Route = selected_item + " to " + destination
        query = f"SELECT * FROM redbus.ap  WHERE Route_Name ='{Route}'"
        bus_df = fetch_data(query)

        count_buses = len(bus_df)
        st.write(f"{count_buses} Buses Available")

        if not bus_df.empty:
            st.markdown("<h2 style='text-align: center; color: black;'>Available Buses</h2>", unsafe_allow_html=True)

            st.sidebar.header("Filter Options")
            sort_by = st.sidebar.selectbox("Sort by", ["Price", "Star_Rating", "Duration", "Departing_Time"])
            sort_order = st.sidebar.radio("Order", ["Ascending", "Descending"])
            ascending = True if sort_order == "Ascending" else False

            sorted_bus_df = bus_df.sort_values(by=sort_by, ascending=ascending)

            for _, row in sorted_bus_df.iterrows():
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.write(f"### {row['Bus_Name']} - {row['Bus_Type']}")
                    st.write(f"**Departing Time:** {row['Departing_Time']}  |  **Reaching Time:** {row['Reaching_Time']}")
                    st.write(f"**Duration:** {row['Duration']}  |  **Star Rating:** {row['Star_Rating']} ⭐")
                    st.write(f"**Price:** ₹{row['Price']}  |   **Seat Availability:** {row['Seat_Availability']}")
                    st.write(f"[Book Now]({row['Route_Link']})")
                    st.markdown("---")
        else:
            st.write("No buses available for the selected route.")
    else:
        st.write("No route data available to display.")

if __name__ == "__main__":
    main()
