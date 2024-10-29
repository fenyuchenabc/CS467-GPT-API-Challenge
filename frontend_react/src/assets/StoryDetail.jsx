import React from 'react';
import { useParams } from 'react-router-dom';

function StoryDetail() {
  const { id } = useParams();
  
  // Sample content - replace with actual story details fetched from an API or database
  const storyContent = `This is the content of Story ${id}`;

  return (
    <div className="story-detail-page">
      <h2>Story {id}</h2>
      <p>{storyContent}</p>
    </div>
  );
}

export default StoryDetail;