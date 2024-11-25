import streamlit as st
import requests


def main():
    """
    Streamlit frontend for the "Create New Story" feature.
    Allows users to input a story idea and select the story length.
    """
    # Page Title and Input Section
    st.title("Create a New Story")
    st.subheader("Length of the Story")

    # Input: Number of pages
    pages = st.selectbox("Select number of pages", [1, 2, 3, 4, 5], help="Choose how long you want the story to be.")

    # Input: Story prompt
    prompt = st.text_area("Enter your story idea", placeholder="Write your creative ideas here...", help="Provide a brief idea or theme for your story.")

    # Button to generate the story
    if st.button("Create Story"):
        # Validate inputs
        if not prompt:
            st.warning("Please provide a story idea")
            return
        
        # API call to backend
        try:
            st.info("Generating your story. Please wait...")
            backend_url = "http://127.0.0.1:5000/create_story"  # Backend API endpoint
            response = requests.post(backend_url, json={"pages": pages, "prompt": prompt})
            
            # Process API response
            if response.status_code == 200:
                response_data = response.json()
                story = response_data.get("story", "No story generated.")
                image_url = response_data.get("image_url", "")

                # Display the generated story
                st.success("Story generated successfully!")
                st.write(story)

                # Display the generated image if available
                if image_url:
                    st.image(image_url, caption="Generated Illustration", use_column_width=True)
                else:
                    st.warning("No image was generated for this story.")
            else:
                st.error(f"Failed to generate story: {response.status_code} - {response.text}")

        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the backend server. Please ensure the Flask backend is running.")
        except requests.exceptions.RequestException as e:
            st.error(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()