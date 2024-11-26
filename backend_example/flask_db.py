from flask import Flask, jsonify, request
from database import StoryDatabase
from flask_cors import CORS
from story_text import Author
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
db = StoryDatabase()
agent = Author()
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow all origins for development


@app.route('/api/start-story', methods=['POST'])
def start_story():
    """
    Starts a new interactive story based on user input.

    Request Body:
    - genre (str): The genre of the story.
    - age (int): The target age group.
    - choice_count (int): Number of choices per segment.
    - page_count (int): Approximate length of the story.
    - key_moments (list[str], optional): Key moments to include in the story.

    Returns:
    - JSON with the first page of the story and the generated title.
    """
    try:
        data = request.get_json()
        if not all(key in data for key in ['genre', 'age', 'choice_count', 'page_count']):
            return jsonify({"error": "Missing required fields"}), 400
        
        genre = data['genre']
        age = data['age']
        choice_count = data['choice_count']
        page_count = data['page_count']
        key_moments = data.get('key_moments')

        # Extract the title from the first line of the story
        story = agent.first_page(genre, age, choice_count, page_count, key_moments)
        title = story.split("\n")[0].strip()
        if not title.startswith("Title: "):  # Validate title prefix
            title = "Untitled Story"
        else:
            title = title.replace("Title: ", "").strip()
            
        response = agent.first_page(genre, age, choice_count, page_count, key_moments)
        return jsonify({"content": response}), 200
    except Exception as e:
        logging.error(f"Error in /api/start-story: {e}")
        return jsonify({"error": "Failed to start story"}), 500


@app.route('/api/continue-story', methods=['POST'])
def continue_story():
    """
    Continues the story based on user input.

    Request Body:
    - text (str): The user's choice or input for the next segment.

    Returns:
    - JSON with the next segment of the story.
    """
    try:
        data = request.get_json()
        if 'text' not in data:
            return jsonify({"error": "Missing required field: text"}), 400
        
        user_input = data['text']
        response = agent.execute(user_input)
        return jsonify({"content": response}), 200
    except Exception as e:
        logging.error(f"Error in /api/continue-story: {e}")
        return jsonify({"error": "Failed to continue story"}), 500


@app.route('/api/save-story', methods=['POST'])
def save_story():
    """
    Saves a completed story to the database.

    Request Body:
    - genre (str): Genre of the story.
    - age (int): Target age group.
    - choice_count (int): Number of choices per segment.
    - page_count (int): Length of the story.
    - content (str): The complete story content.

    Returns:
    - Success or error message.
    """
    try:
        data = request.get_json()
        required_fields = ['genre', 'age', 'choice_count', 'page_count', 'content']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        genre = data['genre']
        age = data['age']
        choice_count = data['choice_count']
        page_count = data['page_count']
        content = data['content']

        db.save_story(genre, age, choice_count, page_count, content)
        return jsonify({"message": "Story saved successfully"}), 200
    except Exception as e:
        logging.error(f"Error in /api/save-story: {e}")
        return jsonify({"error": f"Failed to save story: {str(e)}"}), 500


@app.route('/api/stories', methods=['GET'])
def get_stories():
    """
    Retrieves all saved stories from the database.

    Returns:
    - JSON list of all stories with details.
    """
    try:
        # Grab DB Tables
        cursor = db.sqlconn.cursor()
        cursor.execute("SELECT * FROM story_data")
        rows = cursor.fetchall()
        # Convert to dict
        stories = [
            {
                'story_id': row[0],
                'genre': row[1],
                'age': row[2],
                'choice_count': row[3],
                'segment_count': row[4],
                'content': row[5],
            }
            for row in rows
        ]
        # Return json for frontend
        return jsonify(stories), 200
    except Exception as e:
        logging.error(f"Error in /api/stories: {e}")
        return jsonify({"error": "Failed to retrieve stories"}), 500

@app.route('/api/stories/<int:story_id>', methods=['DELETE'])
def delete_story(story_id):
    """
    Deletes a story from the database by its ID.

    Path Parameters:
    - story_id (int): The ID of the story to delete.

    Returns:
    - Success or error message.
    """
    try:
        db.delete_story(story_id)
        return jsonify({"message": "Story deleted successfully"}), 200
    except Exception as e:
        logging.error(f"Error in /api/stories/<int:story_id>: {e}")
        return jsonify({"error": "Failed to delete story"}), 500


if __name__ == '__main__':
    app.run(debug=True)
