import streamlit as st
from pathlib import Path
from CreateStory import main as create_story_main
from History import main as history_main

# Define the path to the image in the utils folder and convert it to a string
image_path = str(Path(__file__).parent / "utils" / "storybook-image.jpg")

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# Define a function to switch pages
def switch_page(page_name):
    st.session_state['page'] = page_name

# Custom CSS for the navigation bar
st.markdown("""
    <style>
    /* Navigation Bar Container */
    .navbar {
        display: flex;
        justify-content: center;
        background-color: #4A4A4A;
        padding: 10px;
        font-family: 'Arial', sans-serif;
    }

    /* Navigation Bar Links */
    .navbar button {
        background: none;
        color: #E5E5E5; /* Light color */
        border: none;
        margin: 0 20px; /* Spacing between links */
        font-size: 18px; /* Font size */
        padding: 8px 16px; /* Padding around links */
        border-radius: 5px; /* Rounded corners */
        transition: background-color 0.3s, color 0.3s; /* Smooth transition */
        cursor: pointer;
    }

    /* Active and Hover Effects for Links */
    .navbar button:hover {
        background-color: #E5E5E5; /* Light color on hover */
        color: #4A4A4A; /* Dark text color on hover */
    }

    /* Centering welcome message */
    .welcome {
        text-align: center;
        margin-top: 30px;
        font-family: 'Arial', sans-serif;
    }

    /* Styling the image */
    .storybook-image {
        display: block;
        margin: 0 auto;
        max-width: 80%;
        border-radius: 15px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Display the navigation bar using buttons
st.markdown("<div class='navbar'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("Home"):
        switch_page("home")
with col2:
    if st.button("Create New Story"):
        switch_page("create")
with col3:
    if st.button("History"):
        switch_page("history")
st.markdown("</div>", unsafe_allow_html=True)

# Page routing based on session state
page = st.session_state['page']

if page == "home":
    # Home page content
    st.markdown("""
        <div class="welcome">
            <h1>Welcome to Storybook GPT</h1>
            <p style="font-size: 18px; max-width: 600px; margin: 0 auto;">
                Welcome to the world of Storybook GPT, where AI brings your imagination to life!
                This platform generates unique stories based on your inputs, blending creativity with technology.
                Dive into the magical realm of AI-driven storytelling and let the adventures begin.
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.image(image_path, use_column_width=True)

elif page == "create":
    # Call the CreateStory page
    create_story_main()

elif page == "history":
    # Call the History page
    history_main()
