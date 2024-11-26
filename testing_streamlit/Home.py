import streamlit as st
from pathlib import Path
from CreateStory import main as create_story_main
from History import main as history_main
from AdventureMode import main as adventure_mode_main

# Initialize session state for page navigation
def initialize_session_state():
    """
    Initialize the session state for page navigation if not already set.
    """
    if 'page' not in st.session_state:
        st.session_state['page'] = 'home'

initialize_session_state()

# Define a function to switch pages
def switch_page(page_name):
    """
    Updates the session state to the selected page.
    
    Parameters:
    - page_name (str): The name of the page to switch to.
    """
    st.session_state['page'] = page_name

# Load custom CSS
def load_css(css_file):
    """
    Loads a CSS file to style the Streamlit app.

    Parameters:
    - css_file (str): Path to the CSS file.
    """
    try:
        with open(css_file, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Error: CSS file not found. Please check the file path.")

# Load CSS from utils folder
css_path = Path(__file__).parent / "utils" / "styles.css"
load_css(css_path)

# Define the path to the image in the utils folder
image_path = Path(__file__).parent / "utils" / "storybook-image.jpg"
if not image_path.exists():
    st.error("Error: Storybook image not found. Please check the file path.")

# Navigation using a sidebar
st.sidebar.title("Storybook GPT Navigation")
page_options = {
    "Home": "home",
    "Create New Story": "create",
    "History": "history",
    "Adventure Mode": "adventure",
}
selected_page = st.sidebar.radio(
    "Choose a page:",
    options=list(page_options.keys()),
    index=list(page_options.values()).index(st.session_state["page"]),
)

# Add a "Go" button in the sidebar to confirm the selection
if st.sidebar.button("Go"):
    # Update the session state with the selected page
    switch_page(page_options[selected_page])

# Route pages based on user selection
def show_home_page():
    """
    Displays the home page with a welcome message and image.
    """
    st.markdown(
        """
        <div class="welcome">
            <h1>Welcome to Storybook GPT</h1>
            <p style="font-size: 18px; max-width: 600px; margin: 0 auto;">
                Welcome to the world of Storybook GPT, where AI brings your imagination to life!
                This platform generates unique stories based on your inputs, blending creativity with technology.
                Dive into the magical realm of AI-driven storytelling and let the adventures begin.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.image(str(image_path), caption="Welcome to Storybook GPT", use_column_width=True)


# Page dictionary for routing
pages = {
    "home": show_home_page,
    "create": create_story_main,
    "history": history_main,
    "adventure": adventure_mode_main,
}

# Display the selected page
try:
    pages[st.session_state["page"]]()
except Exception as e:
    st.error(f"Error loading the page: {st.session_state['page']}")
    st.session_state["page"] = "home"