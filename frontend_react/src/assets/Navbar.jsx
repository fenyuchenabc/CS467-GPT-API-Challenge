import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="logo">StoryBook GPT</div>
      <ul className="nav-links">
        <li><Link to="/">Home</Link></li>
        <li><Link to="/newstory">Create New Story</Link></li>
        <li><Link to="/history">History</Link></li>
      </ul>
    </nav>
  );
}

export default Navbar;