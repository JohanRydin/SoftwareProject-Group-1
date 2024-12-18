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
        {userName!=null && <button className={`nav-item ${displayMyList ? 'nav-item-mylist-active' : 'nav-item-mylist'}`}
          onClick={() => {
            setDisplayMyList(!displayMyList)
            setDisplayWishlist(false)
            setSearchQuery('')
          }}
        >
          <ThumbUp></ThumbUp>
        </button>}
        {userName!=null && <button className={`nav-item ${displayWishlist ? 'nav-item-wishlist-active' : 'nav-item-wishlist'}`}
          onClick={() => {
            setDisplayWishlist(!displayWishlist)
            setDisplayMyList(false)
            setSearchQuery('')
          }}
        >
          {displayWishlist ? <FavoriteIcon/>: <FavoriteBorderIcon/>}
        </button>}
        {userName!=null && <GenreDropdown  userName={userName}/>}
        
        <form onSubmit={handleSubmit} className="search-form">
          <input
            type="text"
            placeholder="Search games..."
            value={inputValue}
            onChange={onChange}
            className="search-input"
          />
          <button type="submit" className="search-button">
            <SearchIcon className="search-icon" onClick={searchStart} />
          </button>
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