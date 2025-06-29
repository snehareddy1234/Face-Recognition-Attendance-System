
import streamlit as st
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="FRAS",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .header {
        background-color: #1c1c1c;
        color: white;
        padding: 20px;
        text-align: center;
        border-radius: 8px;
        margin-bottom: 30px;
    }
    .stButton>button {
        background-color: #1c1c1c;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Display logo and title
logo = Image.open("assets/logo.jpg")
st.image(logo, width=1080*1080)
st.markdown('<div class="header"><p>Attendance Management System</p></div>', unsafe_allow_html=True)

# Main description
st.write("""
FRAS - a smart attendance system using face recognition.
Navigate to different sections using the sidebar menu.
""")
