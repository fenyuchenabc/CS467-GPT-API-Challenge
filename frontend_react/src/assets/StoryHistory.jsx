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

  return (
    // Need to change DB entry to take title as well instead of using story ID
    <div className="story-history">
      <h1>Stories</h1>
      {stories.map((story) => (
        <div key={story.story_id} className="story-item"> 
          <h2>Genre: {story.genre}</h2>
          <p>Age: {story.age}</p>
          <p>Choice Count: {story.choice_count}</p>
          <p>Segment Count: {story.segment_count}</p>
          <p>{story.content}</p>
        </div>
      ))}
    </div>
  );
}

export default StoryList;
