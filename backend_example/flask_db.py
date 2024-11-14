from flask import Flask, jsonify, request
from database import StoryDatabase
from flask_cors import CORS
from story_text import Author

app = Flask(__name__)
db = StoryDatabase()
agent = Author()
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow all origins for development


@app.route('/api/start-story', methods=['POST'])
def start_story():
    data = request.get_json()
    genre = data['genre']
    age = data['age']
    choice_count = data['choice_count']
    page_count = data['page_count']
    key_moments = data.get('key_moments')

    response = agent.first_page(genre, age, choice_count, page_count, key_moments)
    return jsonify({"content": response})


@app.route('/api/continue-story', methods=['POST'])
def continue_story():
    data = request.get_json()
    user_input = data['text']

    response = agent.execute(user_input)
    return jsonify({"content": response})


@app.route('/api/save-story', methods=['POST'])
def save_story():
    data = request.get_json()
    genre = data['genre']
    age = data['age']
    choice_count = data['choice_count']
    page_count = data['page_count']
    content = data['content']

    try:
        db.save_story(genre, age, choice_count, page_count, content)
        return jsonify({"message": "Story saved successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to save story: {e}"}), 500


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

@app.route('/api/stories/<int:story_id>', methods=['DELETE'])
def delete_story(story_id):
    db.delete_story(story_id)
    return jsonify({"message": "Story deleted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)
