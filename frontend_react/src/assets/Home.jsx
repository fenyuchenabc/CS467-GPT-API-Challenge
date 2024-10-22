import React from 'react';
import './Home.css';
import StorybookImage from './storybook-image.jpg';

function Home() {
  return (
    <div className="home-container">
      <h1 className="main-title">Welcome to Storybook GPT</h1>
      <p className="intro-text">
        Welcome to the world of Storybook GPT, where AI brings your imagination to life! 
        This platform generates unique stories based on your inputs, blending creativity with technology. 
        Dive into the magical realm of AI-driven storytelling and let the adventures begin.
      </p>
      <div className="image-container">
        <img 
          src={StorybookImage} 
          alt="Storybook theme illustration" 
          className="storybook-image" 
        />
      </div>
    </div>
  );
}

export default Home;
