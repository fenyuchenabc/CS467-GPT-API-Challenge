import unittest
from unittest.mock import patch, MagicMock
from backend_example.story_text import Author
from backend_example.database import StoryDatabase

class TestAuthor(unittest.TestCase):
    @patch("story_text.OpenAI")
    @patch("story_text.StoryDatabase")
    def setUp(self, MockDatabase, MockOpenAI):
        # Mock the OpenAI and Database instances to avoid real connections
        self.mock_db = MockDatabase.return_value
        self.mock_client = MockOpenAI.return_value
        self.mock_assistant = MagicMock()
        self.mock_client.beta.assistants.create.return_value = self.mock_assistant
        self.mock_thread = MagicMock()
        self.mock_assistant.threads.create.return_value = self.mock_thread
        
        # Initialize the Author instance with mocked dependencies
        self.author = Author()

    def test_initialization(self):
        # Verify that OpenAI client and Database were initialized
        self.assertIsNotNone(self.author.client, "OpenAI client should be initialized")
        self.assertIsNotNone(self.author.db, "Database should be initialized")

    @patch("story_text.sleep", return_value=None)  # Mock sleep to speed up test
    def test_execute(self, mock_sleep):
        # Mock the create_message method and the response from API
        message_mock = MagicMock()
        self.mock_thread.messages.create.return_value = message_mock
        run_mock = MagicMock()
        run_mock.status = "completed"
        self.mock_thread.runs.create.return_value = run_mock
        self.mock_thread.runs.retrieve.return_value = run_mock
        message_list_mock = MagicMock()
        message_list_mock.content[0].text.value = "Mocked story content"
        self.mock_thread.messages.list.return_value = [message_list_mock]

        # Run execute and verify the output
        response = self.author.execute("Sample input")
        self.assertEqual(response, "Mocked story content", "The response should match the mocked story content")

    def test_first_page(self):
        # Mock execute to return a sample response
        with patch.object(self.author, 'execute', return_value="Mocked story page content"):
            # Call first_page and verify it attempts to save to the database
            response = self.author.first_page("Fantasy", 10, 3, 5)
            self.assertEqual(response, "Mocked story page content", "The response should match the mocked content")
            self.mock_db.save_story.assert_called_once_with("Fantasy", 10, 3, 5, "Mocked story page content")

    def test_db_close(self):
        # Test that db_close calls the close method on the database
        self.author.db_close()
        self.mock_db.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
