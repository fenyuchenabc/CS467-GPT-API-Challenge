import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  return (
    <nav className="navbar">
      <Link to="/">Home</Link>
      <Link to="/newstory">Create New Story</Link>
      <Link to="/history">History</Link>
    </nav>
  );
}

export default Navbar;
