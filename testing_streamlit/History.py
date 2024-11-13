import streamlit as st
import requests

def main():
    st.title("History")
    st.subheader("Click on a story to view the full content")
    

    # Fetch stories from the backend
    try:
        response = requests.get("http://127.0.0.1:5000/api/stories")
        if response.status_code == 200:
            stories = response.json()

            if stories:
                # Display titles as clickable expanders
                for story in stories:
                    with st.expander(f"📖 {story['genre']} (ID: {story['story_id']})"):
                        st.write(story['content'])
            else:
                st.info("No stories found in the database.")
        else:
            st.error("Failed to retrieve stories. Please try again.")

    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to the backend: {e}")

if __name__ == "__main__":
    main()
