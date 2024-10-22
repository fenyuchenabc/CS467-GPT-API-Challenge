import "./styles.css";
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './assets/Navbar';
import Home from './assets/Home';
import History from './assets/History';
import NewStory from './assets/NewStory';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/history" element={<History />} />
        <Route path="/newstory" element={<NewStory />} />
      </Routes>
    </Router>
  );
}

export default App;