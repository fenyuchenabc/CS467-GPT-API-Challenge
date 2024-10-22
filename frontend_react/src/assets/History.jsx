import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './History.css';

function History() {
  // attribute id for each story
  const [stories, setStories] = useState([
    { id: 1, title: "story1" },
    { id: 2, title: "story2" },
    { id: 3, title: "story3" },
    { id: 4, title: "story4" },
    { id: 5, title: "story5" },
    { id: 6, title: "story6" },
    { id: 7, title: "story7" },
    { id: 8, title: "story8" },
    { id: 9, title: "story9" },
    { id: 10, title: "story10" },
    { id: 11, title: "story11" },
    { id: 12, title: "story12" }
  ]);

  return (
    <div className="history-container">
      <h2 className="title">History</h2>
      <ul className="story-list">
        {stories.map((story) => (
          <li key={story.id} className="story-item">
            <Link to={`/story/${story.id}`} className="story-link">
              <span role="img" aria-label="book">📖</span> {story.title}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default History;
