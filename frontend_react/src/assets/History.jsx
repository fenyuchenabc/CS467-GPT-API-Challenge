import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './History.css';

function History() {
  // attribute id for each story
  const [stories, setStories] = useState([]); // Empty array to hold stories
  const [error, setError] = useState(null);  // Track errors

  useEffect(() => {
    const fetchStories = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/stories'); // Update the URL if needed
        setStories(response.data); // Assuming the API returns an array of stories
      } catch (err) {
        console.error('Error fetching stories:', err);
        setError('Failed to load stories. Please try again later.');
      }
    };

    fetchStories();
  }, []);

  return (
    <div className="history-container">
      <h2 className="title">History</h2>
      {error ? (
        <p className="error">{error}</p> // Display error message if API fails
      ) : (
      <ul className="story-list">
        {stories.map((story) => (
          <li key={story.story_id} className="story-item">
            <Link to={`/story/${story.story_id}`} className="story-link">
              <span role="img" aria-label="book">📖</span> {story.genre} - {story.content.slice(0, 50)}...
            </Link>
          </li>
        ))}
      </ul>
      )}
    </div>
  );
}

export default History;
