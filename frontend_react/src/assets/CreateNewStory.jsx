import React, { useState } from 'react';
import './CreateNewStory.css';

function CreateNewStory() {
  const [pageCount, setPageCount] = useState('');
  const [genre, setGenre] = useState('');
  const [storyText, setStoryText] = useState('');

  const handlePageChange = (e) => {
    setPageCount(e.target.value);
  };
  const handleGenreChange = (e) => {
    setGenre(e.target.value);
  };
  const handleStoryChange = (e) => {
    setStoryText(e.target.value);
  };

  const handleSubmit = () => {
    if (pageCount && storyText) {
      alert(`Story created with ${pageCount} pages: ${storyText}`);
    } else {
      alert('Please fill out both fields.');
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
        <label htmlFor="story-text" className="label">Story Idea</label>
        <textarea 
          id="story-text" 
          className="textarea" 
          placeholder="Put your ideas here" 
          value={storyText} 
          onChange={handleStoryChange}
        />
      </div>

      <button className="submit-btn" onClick={handleSubmit}>
        <span role="img" aria-label="book">📚</span> Create Story
      </button>
    </div>
  );
}

export default CreateNewStory;
