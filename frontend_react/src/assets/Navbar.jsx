import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Navbar.css';


const Navbar = () => {
  const navigate = useNavigate();
  return (
    <nav className="navbar">
      <div className="logo">StoryBook GPT</div>
      <ul className="nav-links">
        <button onClick={() => navigate('/')}>Home</button>
        <button onClick={() => navigate('/newstory')}>Create New Story</button>
        <button onClick={() => navigate('/history')}>History</button>
        <button onClick={() => navigate('/adventuremode')}>Adventure Mode</button>
      </ul>
    </nav>
  );
}

export default Navbar;