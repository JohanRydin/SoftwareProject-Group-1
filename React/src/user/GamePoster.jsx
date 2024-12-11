import React, { useRef, useState, useEffect } from "react";
import './GamePoster.css';
import { getGameImage, postGamePreference, postWishlistGame } from './Connections.jsx';
import AddIcon from '@mui/icons-material/Add';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';

function GamePoster({ userName, gameID, image = null, name = "Cyberpunk 2077", rating = 0, description = '', genres = [], gameDict, onCardClick = null }) {
  const [basedimage, setImage] = useState(image);

  const postGamePref = () => {
    postGamePreference(userName, gameID);
  };
  const postToWishlist = () => {
    postWishlistGame(userName, gameID);
  };

  useEffect(() => {
    const getImage = async () => {
      const gameImage = await getGameImage(name);
      setImage(gameImage);
    };
    getImage();
  }, []);

  return (
    <div className="game-poster">
      {basedimage != null && <img
        onClick={() => { onCardClick({ ...gameDict, image: basedimage }) }}
        src={basedimage}
        alt={name}
        className="poster-image" />}
      <div className="game-info">
        <h3>{name}</h3>
        <div className="buttons">
          <button data-hover-text="Add to My List" onClick={postGamePref}><ThumbUpIcon /></button>
          <button data-hover-text="Add to Wishlist" onClick={postToWishlist}><AddIcon /></button>
        </div>
      </div>
    </div>
  );
}

export default GamePoster;