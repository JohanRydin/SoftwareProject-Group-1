import React, { useRef, useState, useEffect } from "react";
import './GameList.css';
import GamePoster from "./GamePoster.jsx";

function GameList({ games = [], title, userName, onCardClick }) {
  const scrollRef = useRef(null);
  const [isLeftEnd, setIsLeftEnd] = useState(true);
  const [isRightEnd, setIsRightEnd] = useState(false);

  const scroll = (direction) => {
    const { current } = scrollRef;
    const scrollAmount = 1300;
    const scrollOptions = {
      left: direction === "left" ? -scrollAmount : scrollAmount,
      behavior: "smooth",
    };

    current.scrollBy(scrollOptions);
  };

  const handleScroll = () => {
    const { current } = scrollRef;
    setIsLeftEnd(current.scrollLeft <= 1);

    const totalWidth = current.scrollWidth;
    const viewportWidth = current.clientWidth;
    const currentScroll = current.scrollLeft;
    const buffer = 2;

    setIsRightEnd(totalWidth - (currentScroll + viewportWidth) <= buffer);
  };

  useEffect(() => {
    const { current } = scrollRef;
    current.addEventListener('scroll', handleScroll);
    return () => current.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    const observer = new ResizeObserver(() => {
      if (scrollRef.current) {
        handleScroll();
      }
    });

    if (scrollRef.current) {
      observer.observe(scrollRef.current);
      handleScroll();
    }

    return () => observer.disconnect();
  }, []);


  return (
    <div className="gamelist-animator">
      <h2>{title}</h2>
      <div className={`scroll-container ${title === "Liked Games" || title === "Wishlist" ? "special-scroll-container" : ""}`}>
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
      <div className="gamelist-divider"></div>
    </div>
  );
}

export default GameList;
