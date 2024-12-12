import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';
import Button from '@mui/material/Button';
import GenreDropdown from './GenreDropdown.jsx'

const Navbar = ({setSearchQuery, displayMyList, setDisplayMyList, displayWishlist, setDisplayWishlist, setUser, loginModalOpen, setLoginModalOpen, isLoggedIn, setIsLoggedIn}) => {
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
    if (isLoggedIn)
    {
      setIsLoggedIn(false)
      setUser(null)
    }
    else
    {
      setLoginModalOpen(!loginModalOpen)
    }
  };
  const onChange = (e) => {
    setInputValue(e.target.value)
    if(e.target.value == ''){
      setSearchQuery('')
    }

  };

  const genres = [
    "Action", "Adventure", "Comedy", "Drama",
    "Fantasy", "Horror", "Mystery", "Romance",
    "Sci-Fi", "Thriller", "Western", "Biography",
    "Crime", "Documentary", "Animation", "Family",
    "History", "Music", "Sport", "War",
  ];
  const activeGenres = ["Action", "Comedy", "Drama"];

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
        {<GenreDropdown genres={genres} activeGenres={activeGenres}/>}
        
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
        
        <button 
          onClick={handleAuthClick} 
          className="nav-item auth-button"
        >
          {isLoggedIn ? 'Logout' : 'Login'}
        </button>

      </div>
    </nav>
  );
};

export default Navbar;