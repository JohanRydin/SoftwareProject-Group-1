import React, { useRef, useState, useEffect } from "react";
import './GameList.css';
import GamePoster from "./GamePoster.jsx";

function GameList({ games = [], title, userName, onCardClick }) {
    const scrollRef = useRef(null);
    const [isLeftEnd, setIsLeftEnd] = useState(true);
    const [isRightEnd, setIsRightEnd] = useState(false);

    const scroll = (direction) => {
        const { current } = scrollRef;
        const scrollAmount = 1300; // Adjust for the desired scroll distance
        const scrollOptions = {
            left: direction === "left" ? -scrollAmount : scrollAmount,
            behavior: "smooth", // Enables smooth scrolling
        };

        current.scrollBy(scrollOptions);
    };

    const handleScroll = () => {
        const { current } = scrollRef;
        setIsLeftEnd(current.scrollLeft === 0);
        setIsRightEnd(current.scrollWidth - current.scrollLeft === current.clientWidth);
    };

    useEffect(() => {
        const { current } = scrollRef;
        current.addEventListener('scroll', handleScroll);
        return () => current.removeEventListener('scroll', handleScroll);
    }, []);

    return (
        <div className="gamelist-animator">
            <h2>{title}</h2>
            <div className="scroll-container">
                {!isLeftEnd && (
                    <button
                        className="scroll-button left"
                        onClick={() => scroll("left")}
                        aria-label="Scroll Left"
                    >
                        &lt;
                    </button>
                )}
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
                {!isRightEnd && (
                    <button
                        className="scroll-button right"
                        onClick={() => scroll("right")}
                        aria-label="Scroll Right"
                    >
                        &gt;
                    </button>
                )}
            </div>
        </div>
    );
}

export default GameList;