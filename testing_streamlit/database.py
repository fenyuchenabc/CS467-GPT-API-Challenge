import sqlite3

DB_NAME = 'story_db.sqlite'

def get_db_connection():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS stories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_story(title, content):
    """Save a generated story to the database."""
    try:
        conn = get_db_connection()
        print(f"Saving story to DB: title={title}, content={content[:100]}...")  # Print first 100 chars
        conn.execute('INSERT INTO stories (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error in save_story: {e}")


def get_all_stories():
    """Retrieve all stories from the database."""
    conn = get_db_connection()
    stories = conn.execute('SELECT * FROM stories').fetchall()
    conn.close()
    return stories
