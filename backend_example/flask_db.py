from flask import Flask, jsonify
from database import StoryDatabase
from flask_cors import CORS

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


if __name__ == '__main__':
    app.run(debug=True)
