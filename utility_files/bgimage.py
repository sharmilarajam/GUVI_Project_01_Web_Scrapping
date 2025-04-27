import streamlit as st
import base64

@st.cache_data
def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(image_file):
    bin_str = get_base64(image_file)
    page_bg_img = f"""
    <style>
    body {{
        background-image: url("https://thumbs.dreamstime.com/z/passenger-bus-road-tea-plantations-india-munnar-kerala-state-172380611.jpg?w=992,{bin_str}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background("your_local_image.jpg")

# Add some content
st.title("Streamlit with Local Background")
