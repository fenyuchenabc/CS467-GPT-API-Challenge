from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from database import init_db, save_story, get_all_stories
import os
import uuid

# Set api key
load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"
init_db()

# Global dictionary to hold story context per session
story_contexts = {}

class Author:
    def __init__(self):
        writer_job = """You are an accomplished children's story writer. You like to write with a style that is appropriate for children but 
is still interesting to read. Your job is to create stories. Along with the 
story, write an extensive description of each character's detailed description, and any other significant characteristics. Write an extensive description of 
what settings in the story look like as well.
"""
        # Set OpenAI API key
        self.client = OpenAI(api_key=os.getenv("GPT_API_KEY"))
        self.model = 'gpt-4o-mini-2024-07-18'  
    
    def execute(self, text_input):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an accomplished children's story writer."},
                    {"role": "user", "content": text_input}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

    def first_page(self, prompt, pages):
        command = f"Write a story about {prompt}. Make sure it is exactly {pages} page(s) long, one page is around 300 words and please no page number in the contents"
        response = self.execute(command)
        return response

    def start_adventure_story(self, genre, age, choice_count, segment_count):
        command = f"""Write the first page of an interactive {genre} story for a {age}-year-old child.
                      Provide {choice_count} choices per story segment. Only create one segment at a time 
                      and move to the next only after the reader chooses. Limit the story to {segment_count} segments overall."""
        return self.execute(command)

    def continue_adventure_story(self, previous_context, user_input):
        command = f"{previous_context} The user chose option {user_input}. Continue the story from here."
        return self.execute(command)


agent = Author()

# Define the /create_story route
@app.route('/create_story', methods=['POST'])
def create_story():
    try:
        # Get user input from request
        data = request.json
        prompt = data.get('prompt')
        pages = data.get('pages')

        # Validate input
        if not pages or not prompt:
            return jsonify({"error": "Missing 'pages' or 'prompt'"}), 400

        # Generate the first page of the story
        story = agent.first_page(pages, prompt)
        save_story(prompt, story)
        return jsonify({'story': story})

    except Exception as e:
        return jsonify({"error": f"Unexpected server error: {str(e)}"}), 500

@app.route('/get_stories', methods=['GET'])
def get_stories():
    stories = get_all_stories()
    stories_list = [{'id': story['id'], 'title': story['title'], 'content': story['content']} for story in stories]
    return jsonify(stories_list)

# Define the /start_story route for Adventure Mode
@app.route('/start_story', methods=['POST'])
def start_story():
    data = request.json
    genre = data.get('genre')
    age = data.get('age')
    page_count = data.get('page_count')
    choice_count = data.get('choice_count')

    if not (genre and age and page_count and choice_count):
        return jsonify({"error": "Missing required adventure story parameters"}), 400

    # Generate the first page of the adventure story
    story = agent.start_adventure_story(genre, age, choice_count, page_count)

    # Create a unique session ID and store the story context
    session_id = str(uuid.uuid4())
    story_contexts[session_id] = story  # Store initial story in context

    return jsonify({'session_id': session_id, 'story': story})

# Define the /continue_story route for continuing Adventure Mode
@app.route('/continue_story', methods=['POST'])
def continue_story():
    data = request.json
    user_input = data.get('user_input')
    session_id = data.get('session_id')

    if not user_input or not session_id:
        return jsonify({"error": "Missing 'user_input' or 'session_id'"}), 400

    # Retrieve the previous story context
    previous_context = story_contexts.get(session_id, "")
    if not previous_context:
        return jsonify({"error": "Invalid session_id"}), 400

    # Continue the story based on the user's choice
    story = agent.continue_adventure_story(previous_context, user_input)

    # Update the story context with the new part of the story
    story_contexts[session_id] = previous_context + f" User chose option {user_input}. " + story

    return jsonify({'story': story})

# Define the /exit_story route for Adventure Mode
@app.route('/exit_story', methods=['POST'])
def exit_story():
    session_id = request.json.get('session_id')
    if session_id and session_id in story_contexts:
        # Remove the session from the context
        del story_contexts[session_id]
    return jsonify({'message': 'Adventure mode session ended successfully.'})

if __name__ == '__main__':
    print("Flask app started...")
    app.run(debug=True, port=5000)
