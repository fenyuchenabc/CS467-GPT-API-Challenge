import "./styles.css";
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './assets/Navbar';
import Home from './assets/Home';
import History from './assets/History';
import CreateNewStory from './assets/CreateNewStory';
import StoryDetail from './assets/StoryDetail';
import StoryHistory from './assets/StoryHistory';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/history" element={<History />} />
        <Route path="/newstory" element={<CreateNewStory />} />
        <Route path="/history/:id" element={<StoryDetail />} />
        <Route path="/storyhistory" element={<StoryHistory />} />
      </Routes>
    </Router>
  );
}

export default App;