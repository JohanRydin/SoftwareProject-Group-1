import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';
import Button from '@mui/material/Button';

const Navbar = ({setSearchQuery, displayMyList, setDisplayMyList, displayWishlist, setDisplayWishlist}) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);  
  const [inputValue, setInputValue] = useState('');

  //TODO: handleSubmit and handleAutClick is from the odin proj, should be changed.
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Searching for:', inputValue);
    setSearchQuery(inputValue);
    setDisplayWishlist(false)
    setDisplayMyList(false)
  };

  const handleAuthClick = () => {
    setIsLoggedIn(!isLoggedIn);
  };
  const onChange = (e) => {
    setInputValue(e.target.value)
    if(e.target.value == ''){
      setSearchQuery('')
    }

  };

  return (
    <nav className="navbar">
      <div className="nav-items">
        <h1 className="nav-item logo" >GameHive</h1>
        <button className="nav-item"
          onClick={() => {setDisplayMyList(!displayMyList)
            setDisplayWishlist(false)
            setSearchQuery('')
          }}
          style={{background : displayMyList ? '#04820a63': '#4a4a4a63'}}
        >
          My List
        </button>
        <button className="nav-item"
          onClick={() => {setDisplayWishlist(!displayWishlist)
            setDisplayMyList(false)
            setSearchQuery('')
          }}
          style={{background : displayWishlist ? '#04820a63': '#4a4a4a63'}}
        >
          Wishlist
        </button>

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
            value={inputValue}
            onChange={onChange}
            className="search-input"
          />
          <button type="submit" className="search-button">Search</button>
        </form>

      </div>
    </nav>
  );
};

export default Navbar;