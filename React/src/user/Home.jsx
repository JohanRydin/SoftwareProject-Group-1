import React, { useState, useEffect } from 'react';
import './Home.css';
import GameList from './GameList'
import { getRecommendations, getWishList } from './Connections.jsx'

const gameData = {
  gameId: 1,
  name: "cod444",
  genres: ["action", "adventure"],
  description: "Call of Duty is a fast paced action game that recreates various historical battles of modern times: second world war, Iraqi war etc...",
  publisher: "gamehive production",
  ranking: 10
};

const Modal = ({ isOpen, onClose, game }) => {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <button className="close-button" onClick={onClose}>×</button>
        <h2>{game.name}</h2>
        <p>Genres: {game.genres.join(", ")}</p>
        <p>Description: {game.description}</p>
        <p>Publisher:{game.publisher}</p>
        <p>Ranking: {game.ranking}</p>
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