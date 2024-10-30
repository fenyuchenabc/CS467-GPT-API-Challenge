import unittest
import sqlite3
from backend_example.database import StoryDatabase

class TestStoryDatabase(unittest.TestCase):
    def setUp(self):
        # Use an in-memory SQLite database for testing purposes
        self.db = StoryDatabase()
        self.db.sqlconn = sqlite3.connect(':memory:')  # Switch to in-memory database
        self.db.create_table()

    def tearDown(self):
        # Close the database connection after each test
        self.db.close()

    def test_create_table(self):
        # Test if the table is created successfully
        cursor = self.db.sqlconn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='story_data';")
        table = cursor.fetchone()
        self.assertIsNotNone(table, "The story_data table should exist in the database")

    def test_save_story(self):
        # Test saving a story and verifying its insertion
        genre = "Fantasy"
        age = 10
        choice_count = 3
        segment_count = 5
        content = "Once upon a time in a magical forest..."

        # Save the story to the database
        self.db.save_story(genre, age, choice_count, segment_count, content)
        
        # Retrieve the saved story
        cursor = self.db.sqlconn.cursor()
        cursor.execute("SELECT * FROM story_data")
        result = cursor.fetchone()

        # Assert that the result matches the input data
        self.assertIsNotNone(result, "The story should be saved and retrievable from the database")
        self.assertEqual(result[1], genre)
        self.assertEqual(result[2], age)
        self.assertEqual(result[3], choice_count)
        self.assertEqual(result[4], segment_count)
        self.assertEqual(result[5], content)

    def test_close(self):
        # Test that the close method does not raise any exceptions
        try:
            self.db.close()
            closed_successfully = True
        except Exception:
            closed_successfully = False
        self.assertTrue(closed_successfully, "Database should close without errors")

if __name__ == '__main__':
    unittest.main()
