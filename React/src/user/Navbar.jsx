import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';
import Button from '@mui/material/Button';
import GenreDropdown from './GenreDropdown.jsx'
import { getGenres, getGenrePreferences } from './Connections.jsx'
import AccountBoxIcon from "@mui/icons-material/AccountBox";
import QuestionProfile from '@mui/icons-material/MeetingRoom';
import SearchIcon from "@mui/icons-material/Search";
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import FavoriteIcon from '@mui/icons-material/Favorite';
import ThumbUp from '@mui/icons-material/ThumbUp';

const Navbar = ({ setSearchQuery, displayMyList, setDisplayMyList, displayWishlist, setDisplayWishlist, userName, setUser, loginModalOpen, setLoginModalOpen, isLoggedIn, setIsLoggedIn }) => {
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
  
  const searchStart = () => {
    alert("Search functinality here (if user presses button instead of pressing Enter")
  }

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
          <ThumbUp></ThumbUp>
        </button>
        <button className="nav-item"
          onClick={() => {
            setDisplayWishlist(!displayWishlist)
            setDisplayMyList(false)
            setSearchQuery('')
          }}
          style={{ background: displayWishlist ? '#04820a63' : '#4a4a4a63' }}
        >
          {displayWishlist ? <FavoriteIcon/>: <FavoriteBorderIcon/>}
        </button>
        {userName!=null && <GenreDropdown userName={userName}/>}
        
        <form onSubmit={handleSubmit} className="search-form">
          <input
            type="text"
            placeholder="Search games..."
            value={inputValue}
            onChange={onChange}
            className="search-input"
          />
          <SearchIcon sx={{ color: 'black', width: '2%', height: '80%', minWidth: '40px', minHeight: '40px' }} onClick={searchStart} />

        </form>

        <button
          onClick={handleAuthClick}
          className="nav-item"
        >
          {isLoggedIn ? <AccountBoxIcon /> : <QuestionProfile />}
        </button>

      </div>
    </nav>
  );
};

export default Navbar;