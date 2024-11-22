import streamlit as st
import requests
import re

def main():
    st.title("Adventure Mode")
    st.subheader("Start a Choose-Your-Own-Adventure Story")

    # Story setup inputs
    genre = st.selectbox("Select Genre", ["Fantasy", "Sci-Fi", "Mystery", "Adventure"])
    age = st.slider("Select Age", 5, 12, 8)
    choice_count = st.slider("Number of Choices per Segment", 2, 4, 3)
    segment_count = st.slider("Total Segments", 1, 5, 3)

    # Initialize session state for story and options
    if "story" not in st.session_state:
        st.session_state["story"] = ""
    if "options" not in st.session_state:
        st.session_state["options"] = []
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = None  # This will store the session ID from the backend

    # Start story and display initial content with options
    if st.button("Start Story"):
        response = requests.post("http://127.0.0.1:5000/start_story", json={
            "genre": genre,
            "age": age,
            "page_count": segment_count,
            "choice_count": choice_count
        })

        if response.status_code == 200:
            # Capture the session ID and initial story
            data = response.json()
            st.session_state["session_id"] = data.get("session_id")
            st.session_state["story"] = data.get("story", "")
            st.session_state["options"] = list(range(1, choice_count + 1))  # Options 1 to choice_count
            st.write("Story started successfully!")
            st.write(st.session_state["story"])
        else:
            st.error("Failed to start the story. Try again.")

    # Check if story, options, and session_id are set in session state
    if st.session_state["story"] and st.session_state["options"] and st.session_state["session_id"]:
        st.write(st.session_state["story"])

        # Display each option as a button
        for i, option in enumerate(st.session_state["options"], 1):
            if st.button(f"Option {i}"):
                # Send selected option to backend with session_id
                response = requests.post("http://127.0.0.1:5000/continue_story", json={
                    "user_input": str(i),
                    "session_id": st.session_state["session_id"]
                })

                if response.status_code == 200:
                    # Update story and options with new content and choices
                    next_segment = response.json().get("story", "")
                    st.session_state["story"] = next_segment
                    st.session_state["options"] = list(range(1, choice_count + 1))  # Reset options
                    st.write("Story continued successfully!")
                    st.write(next_segment)
                else:
                    st.error("Failed to continue the story. Try again.")
                    st.write(f"Error details: {response.text}")

    # Exit button to end the session
    if st.button("Exit Story"):
        response = requests.post("http://127.0.0.1:5000/exit_story")
        if response.status_code == 200:
            st.success("Adventure Mode session ended.")
            st.session_state.clear()  # Clear session state on exit
        else:
            st.error("Failed to end the session.")

def extract_options(story_text):
    """Extracts numbered options from the story text."""
    # Regex pattern to find options like "1. Option text"
    option_pattern = r"\d+\.\s(.+)"
    options = re.findall(option_pattern, story_text)
    return options


if __name__ == "__main__":
    main()
