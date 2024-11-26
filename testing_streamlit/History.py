import streamlit as st
import requests
from dotenv import load_dotenv
import os
import re

# Load environment variables
load_dotenv()

# Backend API base URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:5000")

def fetch_stories():
    """
    Fetches the list of stories from the backend.

    Returns:
    - list[dict]: A list of story dictionaries if successful.
    - None: If an error occurs or the request fails.
    """
    try:
        response = requests.get(f"{API_BASE_URL}/api/stories")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: Received status code {response.status_code} from the server.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to the backend: {e}")
        return None

def extract_title(content):
    """
    Extracts the title from the content if present, otherwise returns 'Untitled Story'.

    Parameters:
    - content (str): The story content.

    Returns:
    - str: The extracted title or 'Untitled Story'.
    """
    if content:
        # Match a title in the format "**Title: XYZ**" or "Title: XYZ"
        match = re.search(r"(?:\*\*Title: (.*?)\*\*|Title: (.*?)(?=\n|$))", content)
        if match:
            # Return the first matching group that's not None
            return match.group(1) or match.group(2)
    return "Untitled Story"

def display_story(story):
    """
    Displays a single story in an expander widget.

    Parameters:
    - story (dict): A dictionary containing the story details.
    """
    content = story.get("content", "No content available.")
    title = story.get("title", None) or extract_title(content)  # Extract title if not provided
    image_url = story.get("image_url")

    with st.expander(f"📖 {title}"):
        st.write(f"**Genre:** {story.get('genre', 'Unknown')} | **Age Group:** {story.get('age', 'Unknown')}")
        st.write(content)
        if image_url and image_url.startswith("http"):
            st.image(image_url, caption=f"Illustration for {title}", use_column_width=True)
        elif image_url:
            st.warning(f"Image generation failed: {image_url}")
        else:
            st.warning("No image available for this story.")

def main():
    """
    Main function to render the History page in the Streamlit app.
    """
    st.title("History")
    st.subheader("Click on a story to view the full content")

    # Fetch and display stories
    stories = fetch_stories()
    if stories:
        for story in stories:
            display_story(story)
    elif stories is not None:
        st.info("No stories found in the database.")

if __name__ == "__main__":
    main()