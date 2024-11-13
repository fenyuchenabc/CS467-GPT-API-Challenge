from flask import Flask, jsonify, request
from database import StoryDatabase
from flask_cors import CORS
from story_text import Author

app = Flask(__name__)
db = StoryDatabase()
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow all origins for development


@app.route('/api/stories', methods=['GET'])
def get_stories():
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
        return jsonify(stories)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/create_story', methods=['POST'])
def create_story():
    """
    Generate a story using the Author class and save it to the database.
    Expects JSON payload: { "genre": str, "age": int, "choice_count": int, "length": int }
    """
    try:
        # Parse the JSON request
        data = request.json
        genre = data.get('genre')
        age = data.get('age')
        choice_count = data.get('choice_count')
        length = data.get('length')

        if not all([genre, age, choice_count, length]):
            return jsonify({"error": "All fields (genre, age, choice_count, length) are required."}), 400

        # Create an instance of Author and generate the story
        author = Author()
        story_content = author.first_page(genre, age, choice_count, length)
        author.db_close()

        if story_content and story_content != "Error during story generation":
            return jsonify({"message": "Story created successfully", "story_content": story_content}), 201
        else:
            return jsonify({"error": "Failed to generate story."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
