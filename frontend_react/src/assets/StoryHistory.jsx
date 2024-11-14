import React, { useEffect, useState } from 'react';


function StoryList() {
  const [stories, setStories] = useState([]);
  // Connect to flask backend and grab DB
  useEffect(() => {
    fetch('http://localhost:5000/api/stories')
      .then((response) => response.json())
      .then((data) => setStories(data))
      .catch((error) => console.error('Error connecting to stories DB:', error));
  }, []);

  const deleteStory = (story_id) => {
    fetch(`http://localhost:5000/api/stories/${story_id}`, {
      method: 'DELETE',
    })
      .then(fetchStories)
      .catch((error) => console.error('Error deleting story:', error));
  };

  return (
    // Need to change DB entry to take title as well instead of using story ID
    <div className="story-management">
      <h1>Manage Stories</h1>
      
      {/* Table for displaying stories */}
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Genre</th>
            <th>Age</th>
            <th>Choice Count</th>
            <th>Segment Count</th>
            <th>Content</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {stories.map((story) => (
            <tr key={story.story_id}>
              <td>{story.story_id}</td>
              <td>{story.genre}</td>
              <td>{story.age}</td>
              <td>{story.choice_count}</td>
              <td>{story.segment_count}</td>
              <td>{story.content}</td>
              <td>
                <button onClick={() => deleteStory(story.story_id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      </div>
  );
}

export default StoryList;
