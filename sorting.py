import streamlit as st
import pandas as pd

# Sample data for demonstration
data = {
    "Bus_Name": ["Bus A", "Bus B", "Bus C"],
    "Bus_Type": ["AC", "Non-AC", "AC"],
    "Departing_Time": ["10:00 AM", "1:00 PM", "5:00 PM"],
    "Reaching_Time": ["2:00 PM", "6:00 PM", "9:00 PM"],
    "Duration": [4, 5, 4],
    "Star_Rating": [4.5, 4.0, 4.8],
    "Price": [500, 450, 600],
    "Seat_Availability": [5, 10, 2],
    "Route_Link": ["http://routeA.com", "http://routeB.com", "http://routeC.com"],
}
bus_df = pd.DataFrame(data)

# Sorting options
st.sidebar.header("Filter Options")
sort_by = st.sidebar.selectbox(
    "Sort by", ["Price", "Star_Rating", "Duration","Departing_Time"]
)
sort_order = st.sidebar.radio("Order", ["Ascending", "Descending"])

# Apply sorting
ascending = True if sort_order == "Ascending" else False
sorted_bus_df = bus_df.sort_values(by=sort_by, ascending=ascending)

# Display sorted data
st.subheader("Detailed Bus Information")
for _, row in sorted_bus_df.iterrows():
    with st.container():
        st.write(f"### {row['Bus_Name']} - {row['Bus_Type']}")
        st.write(f"**Departing Time:** {row['Departing_Time']}  |  **Reaching Time:** {row['Reaching_Time']}")
        st.write(f"**Duration:** {row['Duration']}  |  **Star Rating:** {row['Star_Rating']} ⭐")
        st.write(f"**Price:** {row['Price']}  |   Seat Availability: {row['Seat_Availability']}")
        st.write(f"[Link]({row['Route_Link']})")
        st.markdown("---")  # Separator between bus details
