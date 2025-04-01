import streamlit as st

# CSS to style the button
button_style = """
<style>
button {
    background-color: red;
    color: white;
    font-size: 16px;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
button:hover {
    background-color: darkred;
}
</style>
"""

# Render the button styling
st.markdown(button_style, unsafe_allow_html=True)

# Create the search input and button
search_query = st.text_input("Enter your search query:")

if st.button("Search"):
    if search_query:
        st.write(f"You searched for: **{search_query}**")
    else:
        st.warning("Please enter a search query before clicking search.")
