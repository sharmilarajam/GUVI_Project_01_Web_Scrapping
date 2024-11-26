import streamlit as st
from datetime import date

# Page Config
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

# Journey Search
st.markdown("## Plan Your Journey 🚌")
with st.form("booking_form"):
    col1, col2, col3 = st.columns([3, 3, 2])

    with col1:
        source = st.text_input("From (Source City)")
    with col2:
        destination = st.text_input("To (Destination City)")
    with col3:
        travel_date = st.date_input("Travel Date", min_value=date.today())

    st.markdown("### Preferences")
    col1, col2, col3 = st.columns(3)
    with col1:
        seat_preference = st.selectbox("Seat Preference", ["No Preference", "Window", "Aisle"])
    with col2:
        bus_type = st.selectbox("Bus Type", ["Any", "AC", "Non-AC", "Sleeper", "Seater"])
    with col3:
        show_only = st.checkbox("Show only available buses")

    # Submit Button
    submitted = st.form_submit_button("Search Buses")
    if submitted:
        st.success(f"Searching buses from {source} to {destination} on {travel_date}...")

# Footer
st.markdown("""
    <div class='subtitle'>
    Powered by Streamlit | Designed for Redbus Enthusiasts
    </div>
""", unsafe_allow_html=True)
