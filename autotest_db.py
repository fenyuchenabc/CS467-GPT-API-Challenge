# test_database.py
import unittest
from backend_example.database import StoryDatabase

class TestStoryDatabase(unittest.TestCase):
    def setUp(self):
        # This runs before each test. Initialize a test database here if needed.
        self.db = StoryDatabase()

    def tearDown(self):
        # This runs after each test. You can clear the database or close connections here.
        self.db.close()

    def test_save_story(self):
        # Test saving a story
        genre = "Fantasy"
        age = 8
        choice_count = 3
        segment_count = 5
        content = "Once upon a time..."
        story_id = self.db.save_story(genre, age, choice_count, segment_count, content)
        self.assertIsNotNone(story_id)  # Check that a story ID was returned

    def test_get_story(self):
        # Save a story and then retrieve it
        genre = "Mystery"
        age = 10
        choice_count = 4
        segment_count = 6
        content = "It was a dark and stormy night..."
        story_id = self.db.save_story(genre, age, choice_count, segment_count, content)
        story = self.db.get_story(story_id)  # Assume this function exists
        self.assertEqual(story['genre'], genre)
        self.assertEqual(story['content'], content)

    def test_delete_story(self):
        # Save and then delete a story
        genre = "Adventure"
        age = 7
        choice_count = 2
        segment_count = 4
        content = "A thrilling adventure..."
        story_id = self.db.save_story(genre, age, choice_count, segment_count, content)
        self.db.delete_story(story_id)  # Assume this function exists
        story = self.db.get_story(story_id)
        self.assertIsNone(story)  # Check that story no longer exists

if __name__ == '__main__':
    unittest.main()
