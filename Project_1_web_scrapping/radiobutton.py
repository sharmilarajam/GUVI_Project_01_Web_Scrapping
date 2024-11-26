import streamlit as st
import pandas as pd

# Sample data (could be a DataFrame from your data source)
data = {
    "Flight": ["Flight A", "Flight B", "Flight C", "Flight D"],
    "Price": [500, 400, 600, 450],
    "Duration": [2.5, 3.0, 1.5, 2.0],  # In hours
    "Rating": [4.5, 4.0, 5.0, 4.7],
    "Departure Time": ["2024-11-10 10:00", "2024-11-10 12:00", "2024-11-10 08:00", "2024-11-10 14:00"]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Streamlit multiselect for sorting options
sort_by = st.multiselect("Sort by", ["Price", "Duration", "Rating", "Departure Time"])

# Streamlit selectbox for sort order
sort_order = st.selectbox("Order", ["Ascending", "Descending"])

# Sorting logic
if sort_by:
    if sort_order == "Ascending":
        df_sorted = df.sort_values(by=sort_by, ascending=True)
    else:
        df_sorted = df.sort_values(by=sort_by, ascending=False)
else:
    df_sorted = df  # No sorting if no criteria are selected

# Display the sorted DataFrame
st.write(f"Flights sorted by {', '.join(sort_by)} ({sort_order})")
st.dataframe(df_sorted)
