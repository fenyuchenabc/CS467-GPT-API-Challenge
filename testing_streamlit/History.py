import streamlit as st
import requests

def main():
    st.title("History")
    st.subheader("Click on a story to view the full content")
    

    # Fetch stories from the backend
    try:
        response = requests.get("http://127.0.0.1:5000/get_stories")
        if response.status_code == 200:
            stories = response.json()

            if stories:
                # Display titles as clickable expanders
                for story in stories:
                    with st.expander(f"📖 {story['title']}"):
                        st.write(story['content'])
                    # Display the image if the image_url exists
                    image_url = story.get('image_url')
                    if image_url and image_url.startswith("http"):
                        st.image(image_url, caption=f"Illustration for {story['title']}", use_column_width=True)
                    elif image_url:
                        st.warning(f"Image generation failed: {image_url}")
                    else:
                        st.warning("No image available for this story.")
            else:
                st.info("No stories found in the database.")
        else:
            st.error("Failed to retrieve stories. Please try again.")

    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to the backend: {e}")

if __name__ == "__main__":
    main()
