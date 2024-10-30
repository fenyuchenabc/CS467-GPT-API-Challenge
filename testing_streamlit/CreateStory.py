import streamlit as st
import requests


def main():
    # Streamlit frontend for "Create New Story"
    st.title("Create a New Story")
    st.subheader("Length of the Story")
    pages = st.selectbox("Select number of pages", [1, 2, 3, 4, 5])

    st.subheader("Story")
    prompt = st.text_area("Put your ideas here")

    if st.button("Create Story"):
        if prompt and pages:
            # Send the user input to the Flask backend
            print(f"Sending to backend: pages={pages}, prompt={prompt}")
            response = requests.post("http://127.0.0.1:5000/create_story", json={"pages": pages, "prompt": prompt})

            if response.status_code == 200:
                story = response.json().get("story", "")
                st.success("Story generated successfully!")
                st.write(story)
            else:
                st.error("Failed to generate story. Try again.")
        else:
            st.warning("Please provide both the story prompt and the number of pages.")