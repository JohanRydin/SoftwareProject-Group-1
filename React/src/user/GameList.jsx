import React, { useRef, useState } from "react";
import './GameList.css';
import GamePoster from "./GamePoster.jsx";


function GameList({ games, title }) {
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
        <div>
            <h2>{title}</h2>
            <div className="scroll-container">
                <button
                    className="scroll-button left"
                    onClick={() => scroll("left")}
                    aria-label="Scroll Left"
                >
                    &lt;
                </button>
                <div className="games-posters" ref={scrollRef}>
                    {games.map((game) => (
                        <GamePoster gameID={game.id} image={game.background_image} name={game.name} rating={game.rating}/>
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
        </div>

    );
}

export default GameList;