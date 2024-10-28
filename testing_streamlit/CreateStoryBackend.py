from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

# Set api key
load_dotenv()

app = Flask(__name__)

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
        command = f"""Write a story about {prompt}. The story should have exactly {pages} page(s).
                  Make sure that the story ends within {pages} page(s)."""
        response = self.execute(command)
        return response

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
        story = agent.first_page(pages,prompt)
        return jsonify({'story': story})

    except Exception as e:
        return jsonify({"error": f"Unexpected server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
