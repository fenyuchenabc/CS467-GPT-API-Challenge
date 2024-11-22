import React, { useState } from 'react';
import './CreateNewStory.css';

function CreateNewStory() {
  const [pageCount, setPageCount] = useState('');
  const [genre, setGenre] = useState('');
  const [age, setAge] = useState('');
  const [choiceCount, setChoiceCount] = useState('');
  const [storyText, setStoryText] = useState('');
  const [storyContent, setStoryContent] = useState('');
  const [isStoryActive, setIsStoryActive] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePageChange = (e) => setPageCount(e.target.value);
  const handleGenreChange = (e) => setGenre(e.target.value);
  const handleAgeChange = (e) => setAge(e.target.value);
  const handleChoiceCountChange = (e) => setChoiceCount(e.target.value);
  const handleStoryChange = (e) => setStoryText(e.target.value);

  const handleStartStory = async () => {
    setLoading(true);
    setError(null);
    const response = await fetch('http://localhost:5000/api/start-story', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ genre, age, choice_count: choiceCount, page_count: pageCount, key_moments: storyText })
    });
    const data = await response.json();
    setStoryContent(data.content);
    setIsStoryActive(true);
  };

  const handleContinueStory = async () => {
    setLoading(true);
    setError(null);
    const response = await fetch('http://localhost:5000/api/continue-story', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: storyText })
    });
    const data = await response.json();
    setStoryContent((prev) => `${prev}\n${data.content}`);
    setStoryText('');
  };

  const handleSaveStory = async () => {
    setLoading(true);
    setError(null);
    const response = await fetch('http://localhost:5000/api/save-story', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ genre, age, choice_count: choiceCount, page_count: pageCount, content: storyContent })
    });
    if (response.ok) {
      alert('Story saved successfully!');
    } else {
      alert('Failed to save story.');
    }
  };

  return (
    <div className="create-story-container">
      <h2 className="title">Create a New Story</h2>

      <div className="input-group">
        <label htmlFor="page-count" className="label">Length of the Story</label>
        <select 
          id="page-count" 
          className="dropdown" 
          value={pageCount} 
          onChange={handlePageChange}
        >
          <option value="">Select number of pages</option>
          <option value="1">1 Page</option>
          <option value="2">2 Pages</option>
          <option value="3">3 Pages</option>
          <option value="4">4 Pages</option>
          <option value="5">5 Pages</option>
        </select>
      </div>

      <div className="input-group">
        <label htmlFor="genre" className="label">Genre</label>
        <select 
          id="genre" 
          className="dropdown" 
          value={genre} 
          onChange={handleGenreChange}
        >
          <option value="">Select a genre</option>
          <option value="Adventure">Adventure</option>
          <option value="Fantasy">Fantasy</option>
          <option value="Science Fiction">Science Fiction</option>
          <option value="Mystery">Mystery</option>
          <option value="Educational">Educational</option>
        </select>
      </div>

      <div className="input-group">
        <label htmlFor="age" className="label">Age</label>
        <input 
          type="number" 
          id="age" 
          className="input" 
          placeholder="Enter age" 
          value={age} 
          onChange={handleAgeChange}
        />
      </div>

      <div className="input-group">
        <label htmlFor="choice-count" className="label">Choice Count</label>
        <input 
          type="number" 
          id="choice-count" 
          className="input" 
          placeholder="Enter choice count" 
          value={choiceCount} 
          onChange={handleChoiceCountChange}
        />
      </div>

      <div className="input-group">
        <label htmlFor="story-text" className="label">Story Idea / Next Input</label>
        <textarea 
          id="story-text" 
          className="textarea" 
          placeholder="Enter your story ideas or next choice here" 
          value={storyText} 
          onChange={handleStoryChange}
        />
      </div>

      <div className="button-group">
        <button className="submit-btn" onClick={handleStartStory}>
          <span role="img" aria-label="book">📚</span> Start Story
        </button>
        
        {isStoryActive && (
          <>
            <button className="submit-btn" onClick={handleContinueStory}>
              <span role="img" aria-label="pencil">✏️</span> Continue Story
            </button>
            <button className="submit-btn" onClick={handleSaveStory}>
              <span role="img" aria-label="floppy disk">💾</span> Save Story
            </button>
          </>
        )}
      </div>

      {isStoryActive && (
        <div className="story-content">
          <h3>Story Content</h3>
          <p>{storyContent}</p>
        </div>
      )}
    </div>
  );
}

export default CreateNewStory;
