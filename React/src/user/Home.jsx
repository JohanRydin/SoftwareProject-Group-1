import React, { useState, useEffect } from 'react';
import './Home.css';
import GameList from './GameList'
import { getRecommendations, getWishList } from './Connections.jsx'
import starIcon from './star-icon.svg';  

const gameData = {
  gameId: 1,
  name: "Cyberpunk 2077",
  genres: ["Action", "Adventure", "ARPG"],
  description: "Cyberpunk 2077 is an open-world, action-adventure RPG set in the megalopolis of Night City, where you play as a cyberpunk mercenary wrapped up in a do-or-die fight for survival. Improved and featuring all-new free additional content, customize your character and playstyle as you take on jobs, build a reputation, and unlock upgrades. The relationships you forge and the choices you make will shape the story and the world around you. Legends are made here. What will yours be?",
  publisher: "CD PROJEKT RED",
  ranking: 9
};

const Modal = ({ isOpen, onClose, game }) => {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <button className="close-button" onClick={onClose}>×</button>
        <h2 className="modal-title">{game.name}</h2>
        <hr className="modal-divider" />
        <p className="modal-ranking">
          Rating: {game.ranking} <img src={starIcon} alt="Star Icon" className="star-icon" />
        </p>
        <p className="modal-genres">Genres: {game.genres.join(", ")}</p>
        <p className="modal-description">{game.description}</p>
      </div>
    </div>
  );
};


function Home({searchQuery, displayMyList, displayWishlist, userName}) {
  const [games, setGames] = useState([]);
  const [myList, setMyList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedGame, setSelectedGame] = useState(null);

  const API_KEY = 'cd1fef93051e4872ad6909f179bde3ea';
  const BASE_URL = 'https://api.rawg.io/api';

  useEffect(() => {
    const fetchGames = async () => {
      try {
        /*const response = await fetch(
          `${BASE_URL}/games?key=${API_KEY}&ordering=-rating&page_size=10`, {mode: 'cors'}
        );

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }*/
        
        //const data = await response.json();

        getRecommendations(userName, [{"similar_to_games" : [1,7,3]}, {"best_reviewed" : "Action"}, {"best_sales" : "Adventure"}]).then(data => {
          const games = data.response.games;
          //console.log(games)
          setGames(games);
        })
        
        getWishList(userName).then(data => {
          const _myList = data;
          console.log(_myList)
          setMyList(["Black Myth: Wukong", "Terraria"]);
        })

       //setGames(data.results);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching games:', err);
        setError(true);
        setLoading(false);
      }
    };

    fetchGames();
  }, []);

  const handleCardClick = (game) => {
    setSelectedGame(game);
    setIsModalOpen(true);
  };

  if (loading) {
    return <div className="loading">Loading games...</div>;
  }

  if (error) {
    return <div className="error">Failed to load games...</div>;
  }

  return (
    <div className="home">
      <Modal 
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        game={gameData|| selectedGame}
      />

      {games != [] && <div className="games-row">
        {searchQuery != '' && (<GameList userName={userName} games={games[0]} title={searchQuery} onCardClick={handleCardClick}/>)}
        {userName != '' && displayMyList && (<GameList userName={userName} games={myList} title ={`${userName}'s List`} onCardClick={handleCardClick}/>)}
        {userName != '' && displayWishlist && (<GameList userName={userName} games={games[1]} title ={`${userName}'s Wishlist`} onCardClick={handleCardClick}/>)}
        <GameList userName={userName} games={games[0]} title="Top 1 games" onCardClick={handleCardClick}/>
      </div>}
    </div>
  );
}

export default Home;