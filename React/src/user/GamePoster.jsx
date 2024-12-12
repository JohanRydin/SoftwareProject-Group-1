import React, { useRef, useState, useEffect } from "react";
import './GamePoster.css';
import { getGameImage, postGamePreference, postWishlistGame, deleteGamePreference, deleteWishlistGame } from './Connections.jsx';
import AddIcon from '@mui/icons-material/Add';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import { useGameContext } from './Home';  // Import the context



function GamePoster({ userName, gameID, image = null, name = "Cyberpunk 2077", rating = 0, description = '', genres = [], gameDict, onCardClick = null}) {
  const { myList, setMyList, wishList, setWishlist } = useGameContext();
  const [basedimage, setImage] = useState(image);

  const inMyList = myList.map((game) => game["id"]).includes(gameID);
  const inWishlist = wishList.map((game) => game["id"]).includes(gameID);
  console.log(gameDict)

  const postGamePref = () => {
    if (inMyList) {
      deleteGamePreference(userName, gameID);
      setMyList(myList.filter(item => item.id !== gameID))
    }
    else{
      postGamePreference(userName, gameID);
      setMyList([...myList, gameDict]);
    }
  };
  const postToWishlist = () => {
    if (inWishlist) {
      deleteWishlistGame(userName, gameID);
      setWishlist(wishList.filter(item => item.id !== gameID))
    }
    else{
      postWishlistGame(userName, gameID);
      setWishlist([...wishList, gameDict]);
    }
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
          <button data-hover-text="Add to My List" onClick={postGamePref} style={{ backgroundColor: inMyList ? 'green' : 'gray' }}><ThumbUpIcon /></button>
          <button data-hover-text="Add to Wishlist" onClick={postToWishlist} style={{ backgroundColor: inWishlist ? 'green' : 'gray' }}><AddIcon /></button>
        </div>
      </div>
    </div>
  );
}

export default GamePoster;