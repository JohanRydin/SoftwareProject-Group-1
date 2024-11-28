import React from "react";
import './GameList.css';


function GameList({ games, title }) {
    return (
        <div>
            <h2>{title}</h2>
            <div className="games-posters">
                {games.map((game) => (
                    <div key={game.id} className="game-poster">
                        <img
                            src={game.background_image}
                            alt={game.name}
                            className="poster-image" />
                        <div className="game-info">
                            <h3>{game.name}</h3>
                            <p>Rating: {game.rating}</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default GameList;