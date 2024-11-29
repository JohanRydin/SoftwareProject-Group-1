import React, { useState, useEffect } from 'react';
import './Home.css';
import GameList from './GameList'

function Home({searchQuery}) {
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const API_KEY = 'cd1fef93051e4872ad6909f179bde3ea';
  const BASE_URL = 'https://api.rawg.io/api';

  useEffect(() => {
    const fetchGames = async () => {
      try {
        const response = await fetch(
          `${BASE_URL}/games?key=${API_KEY}&ordering=-rating&page_size=100`
        );

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        setGames(data.results);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching games:', err);
        setError(true);
        setLoading(false);
      }
    };

    fetchGames();
  }, []);

  if (loading) {
    return <div className="loading">Loading games???</div>;
  }

  if (error) {
    return <div className="error">Failed to load games???</div>;
  }

  return (
    <div className="home">
      <div className="games-row">
        {searchQuery != '' && (<GameList games={games} title={searchQuery}/>)}
        <GameList games={games} title="Top 1 games"/>
        <GameList games={games} title="Top 1 games"/>
        <GameList games={games} title="Top 1 games"/>
        <GameList games={games} title="Top 1 games"/>
        <GameList games={games} title="Top 1 games"/>
      </div>
    </div>
  );
}

export default Home;