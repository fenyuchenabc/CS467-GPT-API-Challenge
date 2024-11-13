from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from database import init_db, save_story, get_all_stories
import os

# Set api key
load_dotenv()

app = Flask(__name__)
init_db()

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

    # Adventure Mode: Generate the first page of a choose-your-own-adventure story
    def start_adventure_story(self, genre, age, choice_count, segment_count):
        command = f"""Write the first page of an interactive {genre} story for a {age}-year-old child.
                      Provide {choice_count} choices per story segment. Only create one segment at a time 
                      and move to the next only after the reader chooses. Limit the story to {segment_count} segments overall."""
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

# Adventure Mode: Start a new adventure story
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
    return jsonify({'story': story})

# Adventure Mode: Continue the story based on user choice
@app.route('/continue_story', methods=['POST'])
def continue_story():
    user_input = request.json.get('user_input')
    if not user_input:
        return jsonify({"error": "Missing 'user_input' for continuing story"}), 400
    # Debugging: Print user input
    print(f"Received user input for continuation: {user_input}")

    # Continue the story with user input
    story = agent.execute(user_input)
    return jsonify({'story': story})
    # Debugging: Print the continuation result
    print(f"Continuation result: {story}")

# Adventure Mode: Exit the adventure story session
@app.route('/exit_story', methods=['POST'])
def exit_story():
    return jsonify({'message': 'Adventure mode session ended successfully.'})


if __name__ == '__main__':
    print("Flask app started...")
    app.run(debug=True, port=5000)
