import React, { useState, useEffect, useContext, createContext} from 'react';
import { getGenres, getGenrePreferences } from './Connections.jsx'

const GenreContext = createContext();

export const GenreProvider = ({ children }) => {
  const [genres, setGenres] = useState([]);
  const [likedGenres, setLikedGenres] = useState([]);

  useEffect(() => {
    const fetchGenres = async () => {
      try {
      getGenres('', 40).then(data => {
          setGenres(data);
      })
      }
      catch (e) {
      console.log(e)
      }
    };
    fetchGenres();
    }, []);

  return (
    <GenreContext.Provider value={{ genres, setGenres, likedGenres, setLikedGenres }}>
      {children}
    </GenreContext.Provider>
  );
};

// Hook to Access Context
export const useGenreContext = () => useContext(GenreContext);

// "Globally" set liked genres
export const setGenresPrefs = async (userName, setLikedGenres) => {
  if (userName != null) {
    try {
      const data = await getGenrePreferences(userName);
      setLikedGenres(data);
    } catch (e) {
      console.log(e);
      setLikedGenres([]);
    }
  } else {
    setLikedGenres([]);
  }
};
