import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';
import Button from '@mui/material/Button';
import GenreDropdown from './GenreDropdown.jsx'
import { getGenres, getGenrePreferences } from './Connections.jsx'

const Navbar = ({setSearchQuery, displayMyList, setDisplayMyList, displayWishlist, setDisplayWishlist, userName, setUser, loginModalOpen, setLoginModalOpen, isLoggedIn, setIsLoggedIn}) => {
  const [inputValue, setInputValue] = useState('');
  const [genres, setGenres] = useState([]);
  const [likedGenres, setLikedGenres] = useState([]);

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

  useEffect(() => {
    const fetchGenres = async () => {
      try {
        setGenres(getGenres)// TODO: Fix when endpoint implemented
        /*getGenres().then(data => {
          const _genres = data.response.genres;
          setGenres(_genres);
        })*/
      }
      catch (e) {
        console.log(e)
      }
    };

    fetchGenres();
  }, []);
  useEffect(() => {
    const fetchGenresPrefs = async () => {
      if (userName != null)
      {
        try {
          getGenrePreferences(userName).then(data => {
            setLikedGenres(data);
          })
        }
        catch (e) {
          console.log(e);
          setLikedGenres([]);
        }
      }
      else
      {
        setLikedGenres([]);
      }
    };

    fetchGenresPrefs();
  }, [userName]);

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
        {<GenreDropdown genres={genres} likedGenres={likedGenres} userName={userName}/>}
        
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