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
            page_count INTEGER NOT NULL,
            content TEXT NOT NULL
        )'''

        self.sqlconn.execute(query)
        self.sqlconn.commit()

    def save_story(self, genre, age, page_count, content):
        query = '''INSERT INTO story_data (genre, age, page_count, content)
                VALUES (?, ?, ?, ?)'''

        self.sqlconn.execute(query, (genre, age, page_count, content))
        self.sqlconn.commit()

    def close(self):
        self.sqlconn.close()