
import streamlit as st
from datetime import date



# Set the minimum date to today
min_date = date.today()

# Display a date input widget with restriction to today and future dates
selected_date = st.date_input(
    "Select a date",
    value=min_date,       # Default date set to today
    min_value=min_date    # Restrict past dates
)

# Display the selected date
st.write("You selected:", selected_date)
