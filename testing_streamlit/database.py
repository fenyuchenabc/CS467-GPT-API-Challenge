import sqlite3
import logging
from pathlib import Path

DB_NAME = 'story_db.sqlite'

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_db_connection():
    """
    Establish a connection to the SQLite database.
    
    Returns:
    - sqlite3.Connection: A database connection object.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logging.error(f"Database connection error: {e}")
        raise

def init_db():
    """
    Initialize the database with required tables.
    Creates a 'stories' table if it does not already exist.
    """
    try:
        with get_db_connection as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS stories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    image_url TEXT
                )
            ''')
            logging.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logging.error(f"Error initializing database: {e}")
        raise

def save_story(title, content, image_url=None):
    """
    Save a generated story to the database.
    
    Parameters:
    - title (str): Title of the story.
    - content (str): Content of the story.
    - image_url (str, optional): URL of an associated image for the story.
    
    Returns:
    - bool: True if the story was saved successfully, False otherwise.
    """
    if not title or not content:
        logging.warning("Title and content are required to save a story.")
        return False
    
    try:
        with get_db_connection() as conn:
            conn.execute(
                "INSERT INTO stories (title, content, image_url) VALUES (?, ?, ?)",
                (title, content, image_url),
            )
            logging.info(f"Story saved successfully: {title}")
            return True
    except sqlite3.Error as e:
        logging.error(f"Error saving story: {e}")
        return False


def get_all_stories():
    """
    Retrieve all stories from the database.
    
    Returns:
    - list[dict]: A list of stories, each represented as a dictionary.
    """
    try:
        with get_db_connection() as conn:
            stories = conn.execute("SELECT * FROM stories").fetchall()
            return [dict(story) for story in stories]
    except sqlite3.Error as e:
        logging.error(f"Error fetching stories: {e}")
        return []
