import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';
import Button from '@mui/material/Button';
import GenreDropdown from './GenreDropdown.jsx'
import { getGenres, getGenrePreferences } from './Connections.jsx'
import AccountBoxIcon from "@mui/icons-material/AccountBox";
import LogoutButton from '@mui/icons-material/MeetingRoom';
import SearchIcon from "@mui/icons-material/Search";
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import FavoriteIcon from '@mui/icons-material/Favorite';
import ThumbUp from '@mui/icons-material/ThumbUp';
import { useGenreContext, setGenresPrefs } from './GenreProvider.jsx';

const Navbar = ({ setSearchQuery, displayMyList, setDisplayMyList, displayWishlist, setDisplayWishlist, userName, setUser, loginModalOpen, setLoginModalOpen, isLoggedIn, setIsLoggedIn, refresh,removeCookie}) => {
  const [inputValue, setInputValue] = useState('');
  const { setLikedGenres } = useGenreContext();

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
      removeCookie('user')
      removeCookie('userID')
      setGenresPrefs(null, setLikedGenres)
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
        <button className="nav-item logo" onClick={refresh}>GameHive</button>
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
            <SearchIcon className="search-icon" onClick={handleSubmit} />
          </button>
        </form>

        <button
          onClick={handleAuthClick}
          className={isLoggedIn ? "nav-item" : "nav-item-login"}
        >
          {isLoggedIn ? <LogoutButton /> : "Login"}
        </button>

      </div>
    </nav>
  );
};

export default Navbar;