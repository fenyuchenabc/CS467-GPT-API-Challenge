import sqlite3


class StoryDatabase:
    def __init__(self):
        self.sqlconn = sqlite3.connect('story_data.db')
        self.create_table()

    def create_table(self):
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

    def save_story(self, genre, age, choice_count, segment_count, content):
        query = '''INSERT INTO story_data (genre, age, choice_count, segment_count, content)
                VALUES (?, ?, ?, ?, ?)'''

        self.sqlconn.execute(query, (genre, age, choice_count, segment_count, content))
        self.sqlconn.commit()

    def close(self):
        self.sqlconn.close()