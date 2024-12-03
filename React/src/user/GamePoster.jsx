import React, { useRef, useState, useEffect } from "react";
import './GamePoster.css';
import  {getGameImage, postGamePreference, postWishlistGame} from './Connections.jsx'
import AddIcon from '@mui/icons-material/Add';


function GamePoster({userName, gameID, image, name = "Cyberpunk 2077", rating, description = '', onCardClick = null}) {
    const [basedimage, setImage] = useState(image);

    const postGamePref = () =>{
        postGamePreference(userName, gameID)
    }


    useEffect(() => {
        const getImage = async () => {
            const gameImage = await getGameImage(name)
            setImage(gameImage)
        };
        getImage()
    }, []);

   return( 
        <div className="game-poster" >
        <img
            onClick={onCardClick}
            src={basedimage}
            alt={name}
            className="poster-image" />
        <div className="game-info">
            <h3>{name}</h3>
            <button /*onClick={postGamePref}*/><AddIcon /></button>
        </div>
    </div>
   )
}

export default GamePoster