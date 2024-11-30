import streamlit as st
import requests

def main():
    st.title("Adventure Mode")
    st.subheader("Start a Choose-Your-Own-Adventure Story")

    # Inputs for story configuration
    genre = st.selectbox("Select Genre", ["Fantasy", "Sci-Fi", "Mystery", "Adventure"])
    age = st.slider("Select Age", 5, 12, 8)
    choice_count = st.slider("Number of Choices per Segment", 2, 4, 3)
    segment_count = st.slider("Total Segments", 1, 5, 3)

    # Initialize session state variables
    if "story" not in st.session_state:
        st.session_state["story"] = ""
    if "options" not in st.session_state:
        st.session_state["options"] = list(range(1, choice_count + 1))  # Default initial options
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = None
    if "story_started" not in st.session_state:
        st.session_state["story_started"] = False
    if "last_clicked" not in st.session_state:
        st.session_state["last_clicked"] = None  # Track the last clicked option

    # Start the story
    if st.button("Start Story"):
        if not st.session_state.get("story_started", False):
            response = requests.post("http://127.0.0.1:5000/start_story", json={
                "genre": genre,
                "age": age,
                "page_count": segment_count,
                "choice_count": choice_count
            })

            if response.status_code == 200:
                data = response.json()
                st.session_state["session_id"] = data.get("session_id")
                st.session_state["story"] = data.get("story", "")
                st.session_state["options"] = list(range(1, choice_count + 1))
                st.session_state["story_started"] = True
                st.session_state["last_clicked"] = None
            else:
                st.error("Failed to start the story. Try again.")

    # Display the current story
    if st.session_state.get("story"):
        st.write(st.session_state["story"])  # Always display the most up-to-date story

    # Render the option buttons side by side if the story is ongoing
    if st.session_state.get("story") and "The End!" not in st.session_state["story"]:
        selected_option = None  # Track which button was clicked in this render cycle

        # Create columns for side-by-side buttons
        cols = st.columns(len(st.session_state["options"]))
        for idx, col in enumerate(cols):
            option = st.session_state["options"][idx]
            if col.button(f"Option {option}", key=f"option_{option}"):
                selected_option = option  # Capture the clicked option

        # If an option was clicked, process it
        if selected_option is not None:
            response = requests.post("http://127.0.0.1:5000/continue_story", json={
                "user_input": str(selected_option),
                "session_id": st.session_state["session_id"],
                "choice_count": choice_count,
                "page_count": segment_count
            })

            if response.status_code == 200:
                next_segment = response.json().get("story", "")
                st.session_state["story"] = next_segment  # Update the story
                st.session_state["options"] = list(range(1, choice_count + 1))  # Reset options
            else:
                st.error("Failed to continue the story. Try again.")

            # Display the updated story immediately after processing
            st.write(st.session_state["story"])

    # If the story is over, display a message
    if st.session_state.get("story") and "The End!" in st.session_state["story"]:
        st.write("Your adventure has concluded! You can now exit the story.")

    # Exit the story
    if st.button("Exit Story"):
        if st.session_state.get("session_id"):
            response = requests.post("http://127.0.0.1:5000/exit_story", json={
                "session_id": st.session_state["session_id"]
            })
            if response.status_code == 200:
                st.success("Adventure Mode session ended.")
                st.session_state.clear()
            else:
                st.error("Failed to end the session.")
        else:
            st.warning("No active session to exit.")

if __name__ == "__main__":
    main()