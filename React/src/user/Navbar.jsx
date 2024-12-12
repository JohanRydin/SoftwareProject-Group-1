import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';
import Button from '@mui/material/Button';
import AccountBoxIcon from "@mui/icons-material/AccountBox";
import SearchIcon from "@mui/icons-material/Search";
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import GradeIcon from '@mui/icons-material/Grade';
const Navbar = ({ setSearchQuery, displayMyList, setDisplayMyList, displayWishlist, setDisplayWishlist, setUser, loginModalOpen, setLoginModalOpen, isLoggedIn, setIsLoggedIn }) => {
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
    if (isLoggedIn) {
      setIsLoggedIn(false)
      setUser(null)
    }
    else {
      setLoginModalOpen(!loginModalOpen)
    }
  };
  const onChange = (e) => {
    setInputValue(e.target.value)
    if (e.target.value == '') {
      setSearchQuery('')
    }

  };

  return (
    <nav className="navbar">
      <div className="nav-items">
        <h1 className="nav-item logo" >GameHive</h1>
        <button className="nav-item"
          onClick={() => {
            setDisplayMyList(!displayMyList)
            setDisplayWishlist(false)
            setSearchQuery('')
          }}
          style={{ background: displayMyList ? '#04820a63' : '#4a4a4a63' }}
        >
          <GradeIcon></GradeIcon>
        </button>
        <button className="nav-item"
          onClick={() => {
            setDisplayWishlist(!displayWishlist)
            setDisplayMyList(false)
            setSearchQuery('')
          }}
          style={{ background: displayWishlist ? '#04820a63' : '#4a4a4a63' }}
        >
          <FavoriteBorderIcon></FavoriteBorderIcon>
        </button>

        <form onSubmit={handleSubmit} className="search-form">
          <input
            type="text"
            placeholder="Search games..."
            value={inputValue}
            onChange={onChange}
            className="search-input"
          />
          {/*<button type="submit" className="search-button">Search</button>*/}
        </form>
        <SearchIcon sx={{ color: 'white' }} />

        <button
          onClick={handleAuthClick}
          className="nav-item auth-button"
        >
          {/*isLoggedIn ? 'Logout' : 'Login'*/}
          <AccountBoxIcon></AccountBoxIcon>
        </button>

      </div>
    </nav>
  );
};

export default Navbar;