import React, { useState, useEffect, useContext, createContext} from 'react';
import './Home.css';
import GameList from './GameList'
import { getGamePreferences, getRecommendations, getWishList, getGenrePreferences, getSearch } from './Connections.jsx'
import Modal from './Modal.jsx'
import { SelectRows } from './RowSelector.jsx'
import { useGenreContext, setGenresPrefs } from './GenreProvider.jsx';


const GameContext = createContext();

const GameProvider = ({ children }) => {
  const [myList, setMyList] = useState([]);
  const [wishList, setWishlist] = useState([]);

  return (
    <GameContext.Provider value={{ myList, setMyList, wishList, setWishlist }}>
      {children}
    </GameContext.Provider>
  );
};

// Hook to Access Context
export const useGameContext = () => useContext(GameContext);


const HomeContent = ({ searchQuery, displayMyList, displayWishlist, userName, refreshState }) => {
  const { myList, setMyList, wishList, setWishlist } = useGameContext();
  const [games, setGames] = useState([]);
  const [searchedGames, setSearchedGames] = useState([]);
  const [titles, setTitles] = useState([]);
  //const [myList, setMyList] = useState([]);
  //const [wishList, setwishList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedGame, setSelectedGame] = useState(null);

  const { setLikedGenres, likedGenres } = useGenreContext();
  

  useEffect(() => {
      const fetchGames = async () => {
        var _userName = userName
        try {
          if (userName == null) // TODO: If no user is logged in, set default value. Decide something better later
          {
            _userName = "Erik"
            const commands = [{"best_sales" : "Action"}, {"best_sales" : "Adventure"}, {"best_reviewed" : "Sports & Racing"}, {"best_sales" : "Strategy"}, {"best_sales" : "Simulation"}]
            setTitles(["Top Sellers", "Hot Right Now", "Sports & Racing Games", "Strategy Titles", "Simulate Reality"])
            getRecommendations(_userName, commands).then(data => {
              const games = data.response.games;
              setGames(games);
            })
            setLoading(false);
            return;
          }
          
          // Get game preferences for the user
          const gamePrefs = await getGamePreferences(_userName).then(data => {
            const _myList = data;
            setMyList(_myList);
            return _myList;
          })

          
          if (userName != '') {
            setGenresPrefs(userName, setLikedGenres);
          }

          // Get wishlist for the user
          const _wishlist = await getWishList(_userName).then(data => {
            setWishlist(data)
            return data;
          })

          // Select rows based on the users preferences
          const rows = SelectRows(gamePrefs, likedGenres, _wishlist);
          getRecommendations(_userName, rows[0]).then(data => {
            const games = data.response.games;
            setTitles(rows[1]);
            setGames(games);
          })

        setLoading(false);
      } catch (err) {
        console.error('Error fetching games:', err);
        setError(true);
        setLoading(false);
      }
    };

    fetchGames();
  }, [userName, refreshState]);

  useEffect(()=>{
    
    window.scrollTo({
      top: 0,
      behavior: "smooth", // Makes the scroll smooth
    });
  }, [refreshState])

  useEffect(()=> {
    const searchFunction = async () => {
      if (searchQuery != '') {
        const search = await getSearch(searchQuery, 10).then(data => {
          setSearchedGames(data)
          return data;
        })
      }
    };
    searchFunction();
  }, [searchQuery])

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
        gameDict={selectedGame}
        userName={userName}
      />
      {searchQuery != '' ?
      (<GameList userName={userName} games={searchedGames} title={"Search results for: " + searchQuery} onCardClick={handleCardClick} />)
      :
      (games.length > 0 && <div className="games-row">

        {userName != null && displayMyList && (<GameList userName={userName} games={myList} title ={`${userName}'s List`} onCardClick={handleCardClick}/>)}
        {userName != null && displayWishlist && (<GameList userName={userName} games={wishList} title ={`${userName}'s Wishlist`} onCardClick={handleCardClick}/>)}
        {games.map((game, index) => (
          <GameList
            key={index}
            userName={userName}
            games={game}
            title={titles[index]}
            onCardClick={handleCardClick}
          />
        ))}
      </div>)}
    </div>
  );
}


function Home({ searchQuery, displayMyList, displayWishlist, userName, refreshState }) {
  return (
    <GameProvider>
      <HomeContent 
        searchQuery={searchQuery} 
        displayMyList={displayMyList} 
        displayWishlist={displayWishlist} 
        userName={userName} 
        refreshState={refreshState}
      />
    </GameProvider>
  );
};


export default Home;