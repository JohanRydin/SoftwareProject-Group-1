import React, { useRef, useState } from "react";
import './GameList.css';
import GamePoster from "./GamePoster.jsx";


function GameList({ games = [], title, userName, onCardClick }) {
    const scrollRef = useRef(null);

    const scroll = (direction) => {
        const { current } = scrollRef;
        const scrollAmount = 1300; // Adjust for the desired scroll distance
        const scrollOptions = {
            left: direction === "left" ? -scrollAmount : scrollAmount,
            behavior: "smooth", // Enables smooth scrolling
        };

        current.scrollBy(scrollOptions);
    };


    return (
        <div className="gamelist-animator">
            <h2>{title}</h2>
            <div
                className={`scroll-container ${title === "Liked Games" || title === "Wishlist" ? "special-scroll-container" : ""
                    }`}
            >
                <button
                    className="scroll-button left"
                    onClick={() => scroll("left")}
                    aria-label="Scroll Left"
                >
                    &lt;
                </button>
                <div className="games-posters" ref={scrollRef}>
                    {games.map((game) => (
                        <GamePoster
                            key={game["id"]}
                            gameID={game["id"]}
                            userName={userName}
                            name={game["gamename"]}
                            description={game["description"]}
                            genres={game["genres"]}
                            gameDict={game}
                            onCardClick={onCardClick}
                        />
                    ))}
                </div>
                <button
                    className="scroll-button right"
                    onClick={() => scroll("right")}
                    aria-label="Scroll Right"
                >
                    &gt;
                </button>
            </div>
            <div className="gamelist-divider"></div>
        </div>
    );
}

export default GameList;

