import sqlite3


class StoryDatabase:
    def __init__(self):
        try:
            self.sqlconn = sqlite3.connect('story_data.db', check_same_thread=False)
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

    def close(self):
        self.sqlconn.close()