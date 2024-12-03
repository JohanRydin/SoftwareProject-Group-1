import React, { useRef, useState } from "react";
import './GamePoster.css';

function GamePoster({gameID, image, name, rating, description = '', onCardClick = null}) {
   return( 
        <div key={gameID} className="game-poster">
        <img
            src={image}
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