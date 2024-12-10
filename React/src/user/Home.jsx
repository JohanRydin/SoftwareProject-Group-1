import React, { useState, useEffect } from 'react';
import './Home.css';
import GameList from './GameList'
import { getGamePreferences, getRecommendations, getWishList } from './Connections.jsx'
import Modal from './Modal.jsx'

function Home({searchQuery, displayMyList, displayWishlist, userName}) {
  const [games, setGames] = useState([]);
  const [myList, setMyList] = useState([]);
  const [wishList, setwishList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedGame, setSelectedGame] = useState(null);
  

  useEffect(() => {
      const fetchGames = async () => {
        var commands = [{"similar_to_games" : "all"}, {"best_reviewed" : "Action"}, {"best_sales" : "Adventure"}] // TODO: Make logic to set commands
        var _userName = userName
        try {
          if (userName == null) // TODO: If no user is logged in, set default value. Decide something better later
          {
            _userName = "Erik"
            commands = [{"similar_to_games" : [9]}, {"best_reviewed" : "Action"}, {"best_sales" : "Adventure"}]
          }

          getRecommendations(_userName, commands).then(data => {
            const games = data.response.games;
            setGames(games);
          })
          
          getGamePreferences(_userName).then(data => {
            const _myList = data;
            setMyList(_myList);
          })

          getWishList(_userName).then(data => {
            setwishList(data)
          })

          setLoading(false);
        } catch (err) {
          console.error('Error fetching games:', err);
          setError(true);
          setLoading(false);
        }
    };

    fetchGames();
  }, [userName]);

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
        game={selectedGame}
      />

      {games != [] && <div className="games-row">
        {searchQuery != '' && (<GameList userName={userName} games={games[0]} title={searchQuery} onCardClick={handleCardClick}/>)}
        {userName != '' && displayMyList && (<GameList userName={userName} games={myList} title ={`${userName}'s List`} onCardClick={handleCardClick}/>)}
        {userName != '' && displayWishlist && (<GameList userName={userName} games={wishList} title ={`${userName}'s Wishlist`} onCardClick={handleCardClick}/>)}
        <GameList userName={userName} games={games[0]} title="Top 1 games" onCardClick={handleCardClick}/>
        <GameList userName={userName} games={games[1]} title="Best reviewed action games" onCardClick={handleCardClick}/>
        <GameList userName={userName} games={games[2]} title="Most popular" onCardClick={handleCardClick}/>
      </div>}
    </div>
  );
}

export default Home;