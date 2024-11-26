import streamlit as st
import pandas as pd

# Sample dataset
data = {
    'Flight': ['Flight A', 'Flight B', 'Flight C', 'Flight D', 'Flight E'],
    'Price': [150, 200, 250, 300, 350],
    'Rating': [4.5, 4.0, 3.5, 4.8, 4.2],
    'Duration (hours)': [2, 3.5, 1.5, 5, 4],
    'Departure Time (24hr)': [8, 14, 6, 18, 21]  # Time in 24-hour format
}
df = pd.DataFrame(data)

st.title("Flight Filter App")

# Price filter
min_price, max_price = st.slider(
    'Select Price Range',
    min_value=int(df['Price'].min()),
    max_value=int(df['Price'].max()),
    value=(int(df['Price'].min()), int(df['Price'].max()))
)

# Rating filter
min_rating = st.slider(
    'Select Minimum Rating',
    min_value=float(df['Rating'].min()),
    max_value=float(df['Rating'].max()),
    value=float(df['Rating'].min())
)

# Duration filter
max_duration = st.slider(
    'Select Maximum Duration (in hours)',
    min_value=float(df['Duration (hours)'].min()),
    max_value=float(df['Duration (hours)'].max()),
    value=float(df['Duration (hours)'].max())
)

# Departure time filter
departure_time_range = st.slider(
    'Select Departure Time Range (24-hour format)',
    min_value=int(df['Departure Time (24hr)'].min()),
    max_value=int(df['Departure Time (24hr)'].max()),
    value=(int(df['Departure Time (24hr)'].min()), int(df['Departure Time (24hr)'].max()))
)

# Filter the dataframe
filtered_df = df[
    (df['Price'] >= min_price) & 
    (df['Price'] <= max_price) &
    (df['Rating'] >= min_rating) &
    (df['Duration (hours)'] <= max_duration) &
    (df['Departure Time (24hr)'] >= departure_time_range[0]) &
    (df['Departure Time (24hr)'] <= departure_time_range[1])
]

# Display the filtered results
st.write("Filtered Flights:")
st.dataframe(filtered_df)
