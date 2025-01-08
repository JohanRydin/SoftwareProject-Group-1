import React from 'react';
import './Modal.css';
import starIcon from './star-icon.svg';
import GenreButton from './GenreButton';
import { useGenreContext, handleToggleGenre } from "./GenreProvider.jsx";
import { useGameContext } from './Home';  // Import the context
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import FavoriteIcon from '@mui/icons-material/Favorite';
import {postGamePreference, postWishlistGame, deleteGamePreference, deleteWishlistGame } from './Connections.jsx';



export const Modal = ({ isOpen, onClose, gameDict, userName }) => {
  if (!isOpen) return null;

  // game.genres is a string looking like "['action', 'rpg'...]". Can be parsed as list but we need to replace ' with " first
  const genres = JSON.parse(gameDict.genres.replace(/'/g, '"'));
  const { toggledItems, setToggledItems } = useGenreContext();

  const handleToggle = (item) => {
    handleToggleGenre(item, userName, toggledItems, setToggledItems)
  };

  const { myList, setMyList, wishList, setWishlist } = useGameContext();
  
  const inMyList = myList.map((game) => game["id"]).includes(gameDict.id);
  const inWishlist = wishList.map((game) => game["id"]).includes(gameDict.id);

  const postGamePref = () => {
    if (userName != null)
    {
      const gameID = gameDict.id
      if (inMyList) {
        deleteGamePreference(userName, gameID);
        setMyList(myList.filter(item => item.id !== gameID))
      }
      else{
        postGamePreference(userName, gameID);
        setMyList([...myList, gameDict]);
      }
    }
  };
  const postToWishlist = () => {
    if (userName != null)
    {
      const gameID = gameDict.id
      if (inWishlist) {
        deleteWishlistGame(userName, gameID);
        setWishlist(wishList.filter(item => item.id !== gameID))
      }
      else{
        postWishlistGame(userName, gameID);
        setWishlist([...wishList, gameDict]);
      }
    }
  };


  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <button className="close-button" onClick={onClose}>×</button>
        <h2 className="modal-title">{gameDict["gamename"]}</h2>
        <hr className="modal-divider" />
        <div className="image-container">
          <img src={gameDict.image} alt={gameDict.gamename} className="modal-image" />
            {userName &&
	     <div className="image-buttons">
            <button className={`image-button ${inMyList ? 'in-my-list' : ''}`} onClick={postGamePref}> <ThumbUpIcon /> </button>
            <button className={`image-button ${inWishlist ? 'in-wishlist' : ''}`} onClick={postToWishlist}> {inWishlist ? <FavoriteIcon /> : <FavoriteBorderIcon />} </button>
             </div>
	    }
        </div>
        <hr className="modal-divider" />
        <p className="modal-description">{gameDict["description"]}</p>
        <hr className="modal-divider" />
        <div className="modal-genres">
          <div className="genres-list">
	      {userName ?
	       genres.map((genre) => (
                <GenreButton
                  key={genre}
                  genre={genre}
                  isToggled={toggledItems[genre]}
                  onToggle={handleToggle}
                />
              ))
            : genres.map((genre) => (
                <GenreButton
                  key={genre}
                  genre={genre}
                  isToggled={false}
                  onToggle={() => {}}
                />
              ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Modal;
