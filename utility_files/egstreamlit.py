import streamlit as st
import pandas as pd
Bus_Route= Selected_item +" to "+destination
select * from redbus where Bus_Route=g

# Sample data for bus information
#bus_data = {
    "Bus Name": ["Express Line", "City Connect", "Highway Rider", "Night Owl"],
    "Bus Type": ["AC Sleeper", "Non-AC Seater", "AC Seater", "Sleeper"],
    "Departing Time": ["08:00 AM", "09:30 AM", "01:45 PM", "11:00 PM"],
    "Duration": ["5h 30m", "6h 15m", "4h 50m", "8h 00m"],
    "Reaching Time": ["01:30 PM", "03:45 PM", "06:35 PM", "07:00 AM"],
    "Star Rating": [4.5, 4.0, 3.8, 4.2],
    "Price": ["$25", "$18", "$22", "$30"]
}

# Convert data to DataFrame for easier display
bus_df = pd.DataFrame(bus_data)

# Title for the app
st.title("Bus Information Display")

# Display the data in a table
st.subheader("Available Buses")
st.dataframe(bus_df)

# Alternatively, if you want to display each row separately with more formatting:
st.subheader("Detailed Bus Information")

for i, row in bus_df.iterrows():
    with st.container():
        st.write(f"### {row['Bus Name']} - {row['Bus Type']}")
        st.write(f"**Departing Time:** {row['Departing Time']}  |  **Reaching Time:** {row['Reaching Time']}")
        st.write(f"**Duration:** {row['Duration']}  |  **Star Rating:** {row['Star Rating']} ⭐")
        st.write(f"**Price:** {row['Price']}")
        st.markdown("---")  # Separator between bus details
