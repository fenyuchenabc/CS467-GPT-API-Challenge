import sqlite3


class StoryDatabase:
    def __init__(self, db_path='story_data.db'):
        try:
            self.sqlconn = sqlite3.connect(db_path, check_same_thread=False)
            self.create_table()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def create_table(self):
        try:
            query = '''CREATE TABLE IF NOT EXISTS story_data (
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
            print(f"Error creating table: {e}")

    def save_story(self, genre, age, choice_count, segment_count, content):
        try:
            query = '''INSERT INTO story_data (genre, age, choice_count, segment_count, content)
            VALUES (?, ?, ?, ?, ?)'''

            self.sqlconn.execute(query, (genre, age, choice_count, segment_count, content))
            self.sqlconn.commit()
        except sqlite3.Error as e:
            print(f"Error saving story: {e}")
            return None

    def fetch_story(self, story_id=None, genre=None, age=None):
        """
        Fetches story from the database based on provided criteria.
        
        story_id (int): optional
        genre (str): optional
        age (int): optional
        
        Returns a list of dicts. each dict = a story
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
            print(f"Error fetching story: {e}")
            return None
        
    def fetch_all_stories(self):
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
            print(f"Error fetching all stories: {e}")
            return None

                    
    def close(self):
        self.sqlconn.close()