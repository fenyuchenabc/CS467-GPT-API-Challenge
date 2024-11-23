import sqlite3
import logging


class StoryDatabase:
    def __init__(self, db_path='story_data.db'):
        """
        Initializes the database connection and creates the story table if it does not exist.
        """
        self.db_path = db_path
        try:
            self.sqlconn = sqlite3.connect(db_path, check_same_thread=False)
            self.create_table()
        except sqlite3.Error as e:
            logging.error(f"Error connecting to database at {db_path}: {e}")
            raise

    def create_table(self):
        """
        Creates the story_data table and necessary indexes if they do not already exist.
        """
        try:
            query = '''
            CREATE TABLE IF NOT EXISTS story_data (
                story_id INTEGER PRIMARY KEY AUTOINCREMENT,
                genre VARCHAR(60) NOT NULL,
                age INTEGER NOT NULL,
                choice_count INTEGER NOT NULL,
                segment_count INTEGER NOT NULL,
                content TEXT NOT NULL
            )'''
            self.sqlconn.execute(query)
            self.sqlconn.execute("CREATE INDEX IF NOT EXISTS idx_genre ON story_data (genre)")
            self.sqlconn.execute("CREATE INDEX IF NOT EXISTS idx_age ON story_data (age)")
            self.sqlconn.commit()
        except sqlite3.Error as e:
            logging.error(f"Error creating table: {e}")
            raise

    def save_story(self, genre, age, choice_count, segment_count, content):
        """
        Saves a story to the database.

        Parameters:
        - genre (str): Genre of the story.
        - age (int): Target age group.
        - choice_count (int): Number of choices per story segment.
        - segment_count (int): Total number of segments in the story.
        - content (str): Full text of the story.

        Returns:
        - bool: True if the story was saved successfully, False otherwise.
        """
        if not all(isinstance(arg, (str, int)) for arg in [genre, age, choice_count, segment_count]):
            logging.error("Invalid input types for story fields.")
            return False
        try:
            query = '''INSERT INTO story_data (genre, age, choice_count, segment_count, content)
            VALUES (?, ?, ?, ?, ?)'''

            self.sqlconn.execute(query, (genre, age, choice_count, segment_count, content))
            self.sqlconn.commit()
            return True
        except sqlite3.Error as e:
            logging.error(f"Error saving story: {e}")
            return False

    def fetch_story(self, story_id=None, genre=None, age=None):
        """
        Fetches stories based on optional filters.

        Parameters:
        - story_id (int, optional): ID of the story to fetch.
        - genre (str, optional): Genre filter.
        - age (int, optional): Age filter.

        Returns:
        - list[dict]: A list of matching stories or an empty list if no matches found.
        """
        try:
            query = "SELECT * FROM story_data WHERE 1=1"
            parameters = [] # Lsit for query params

            # append based on args
            if story_id is not None:
                query += " AND story_id = ?"
                parameters.append(story_id)
            if genre is not None:
                query += " AND genre = ?"
                parameters.append(genre)
            if age is not None:
                query += " AND age = ?"
                parameters.append(age)

            cursor = self.sqlconn.execute(query, tuple(parameters))
            results = cursor.fetchall()
            
            # Format the output for readability
            stories = []
            for row in results:
                # New dictionary with story details for each row.
                story = {
                    'story_id': row[0],
                    'genre': row[1],
                    'age': row[2],
                    'choice_count': row[3],
                    'segment_count': row[4],
                    'content': row[5]
                }
                stories.append(story)  # update the story dictionary or list

            return stories # list of stories
        except sqlite3.Error as e:
            logging.error(f"Error fetching story: {e}")
            return []
        
    def fetch_all_stories(self):
        """
        Fetches all stories from the database.

        Returns:
        - list[dict]: A list of all stories.
        """
        try:
            query = "SELECT * FROM story_data"
            cursor = self.sqlconn.execute(query)
            results = cursor.fetchall()
            return [
                {
                    'story_id': row[0],
                    'genre': row[1],
                    'age': row[2],
                    'choice_count': row[3],
                    'segment_count': row[4],
                    'content': row[5],
                }
                for row in results
            ]
        except sqlite3.Error as e:
            logging.error(f"Error fetching all stories: {e}")
            return []

    def delete_story(self, story_id):
        """
        Deletes a story by its ID.

        Parameters:
        - story_id (int): The ID of the story to delete.

        Returns:
        - bool: True if the deletion was successful, False otherwise.
        """
        try:
            query = "DELETE FROM story_data WHERE story_id = ?"
            self.sqlconn.execute(query, (story_id,))
            self.sqlconn.commit()
            return True
        except sqlite3.Error as e:
            logging.error(f"Error deleting story: {e}")
            return False

    def close(self):
        """
        Closes the database connection.
        """
        try:
            self.sqlconn.close()
        except sqlite3.Error as e:
            logging.error(f"Error closing the database: {e}")