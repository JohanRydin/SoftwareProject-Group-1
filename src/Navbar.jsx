import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);  


  //TODO: handleSubmit and handleAutClick is from the odin proj, should be changed.
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Searching for:', searchQuery);
  };

  const handleAuthClick = () => {
    setIsLoggedIn(!isLoggedIn);
  };

  return (
    <nav className="navbar">
      <div className="nav-items">
        <Link to="/" className="nav-item logo">GameHive</Link>
        <Link to="/mylist" className="nav-item">My List</Link>
        <Link to="/wishlist" className="nav-item">Wishlist</Link>

        <button 
          onClick={handleAuthClick} 
          className="nav-item auth-button"
        >
          {isLoggedIn ? 'Logout' : 'Login'}
        </button>
        
        <form onSubmit={handleSubmit} className="search-form">
          <input
            type="text"
            placeholder="Search games..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
          <button type="submit" className="search-button">Search</button>
        </form>

      </div>
    </nav>
  );
};

export default Navbar;