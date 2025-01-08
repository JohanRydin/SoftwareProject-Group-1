import React, { useRef, useState, useEffect } from "react";
import './GamePoster.css';
import { getGameImage, postGamePreference, postWishlistGame, deleteGamePreference, deleteWishlistGame } from './Connections.jsx';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import FavoriteIcon from '@mui/icons-material/Favorite';
import { useGameContext } from './Home';  // Import the context



function truncateText(text, maxLength) {
  if (text.length <= maxLength) {
    return text;
  }
  return text.slice(0, maxLength - 3) + "...";
}

function GamePoster({ userName, gameID, image = null, name = "Cyberpunk 2077", rating = 0, description = '', genres = [], gameDict, onCardClick = null }) {
  const { myList, setMyList, wishList, setWishlist } = useGameContext();
  const [basedimage, setImage] = useState(image);

  const inMyList = myList.map((game) => game["id"]).includes(gameID);
  const inWishlist = wishList.map((game) => game["id"]).includes(gameID);
  //console.log(gameDict)

  const postGamePref = () => {
    if (userName != null)
      {
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

  useEffect(() => {
    const getImage = async () => {
      const gameImage = await getGameImage(name);
      setImage(gameImage);
    };
    getImage();
  }, []);

  return (
    <div className="game-poster">
      {basedimage && (
        <img
          onClick={() => {
            onCardClick({ ...gameDict, image: basedimage });
          }}
          src={basedimage}
          alt={name}
          className="poster-image"
        />
      )}
      <div className="game-info">
        <h3>{truncateText(name, 20)}</h3>
      </div>
		    {userName &&
	<div className="poster-buttons">

        <button className="poster-button" data-hover-text={inMyList ? "Remove from My List" : "Add to My List"} onClick={postGamePref} style={{ backgroundColor: inMyList ? 'green' : '#ffffff8e' }}><ThumbUpIcon /></button>
             <button className="poster-button" data-hover-text={inWishlist ? "Remove from Wishlist" : "Add to Wishlist"} onClick={postToWishlist} style={{ backgroundColor: inWishlist ? 'green' : '#ffffff8e' }}>{inWishlist ? <FavoriteIcon/>: <FavoriteBorderIcon/>}</button>
	    
	</div>
		    }
    </div>
  );
}


export default GamePoster;
