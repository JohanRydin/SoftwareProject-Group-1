import React, { useRef, useState, useEffect } from "react";
import './GamePoster.css';
import  {getGameImage} from './Connections.jsx'

function GamePoster({gameID, image, name = "Cyberpunk 2077", rating, description = '', onCardClick = null}) {
    const [basedimage, setImage] = useState(image);

    useEffect(() => {
        const getImage = async () => {
            const gameImage = await getGameImage(name)
            setImage(gameImage)
        };
        getImage()
    }, []);

   return( 
        <div className="game-poster">
        <img
            src={basedimage}
            alt={name}
            className="poster-image" />
        <div className="game-info">
            <h3>{name}</h3>
            <p>Rating: {rating}</p>
        </div>
    </div>
   )
}

export default GamePoster