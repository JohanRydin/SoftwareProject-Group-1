import React, { useState, useEffect, useContext, createContext} from 'react';
import { getGenres, getGenrePreferences, postGenrePreference, deleteGenrePreference } from './Connections.jsx'

const GenreContext = createContext();

export const GenreProvider = ({ children }) => {
  const [genres, setGenres] = useState([]);
  const [likedGenres, setLikedGenres] = useState([]);
    const [toggledItems, setToggledItems] = useState({});

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

    useEffect(() => {
      const initialToggled = {};
      likedGenres.forEach((genre) => {
        initialToggled[genre] = true;
      });
      setToggledItems(initialToggled);
    }, [likedGenres]);

  return (
    <GenreContext.Provider value={{ genres, setGenres, likedGenres, setLikedGenres, toggledItems, setToggledItems }}>
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

export const handleToggleGenre = (item, userName, toggledItems, setToggledItems) => {
    if (userName != null) {
      if (toggledItems[item]) {
        try {
          deleteGenrePreference(userName, item);
        } catch (e) {
          console.log(e);
        }
      } else {
        try {
          postGenrePreference(userName, item);
        } catch (e) {
          console.log(e);
        }
      }
    }
    setToggledItems((prev) => ({
      ...prev,
      [item]: !prev[item],
    }));
  };
