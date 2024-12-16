import React, { useState, useEffect } from "react";
import "./GenreDropdown.css";
import GenreButton from './GenreButton';
import { useGenreContext, handleToggleGenre } from "./GenreProvider.jsx";

const GenreDropdown = ({ userName }) => {
  const [isDropdownVisible, setIsDropdownVisible] = useState(false);
  const [sortedGenres, setSortedGenres] = useState([]);
  const [columns, setColumns] = useState([]);
  const { genres, toggledItems, setToggledItems } = useGenreContext();

  useEffect(() => {
    setSortedGenres([...genres]);
  }, []);

  useEffect(() => {
    setColumns(
      sortedGenres.reduce((result, genre, index) => {
        const columnIndex = index % 4;
        if (!result[columnIndex]) {
          result[columnIndex] = [];
        }
        result[columnIndex].push(genre);
        return result;
      }, [])
    );
  }, [sortedGenres]);

  useEffect(() => {
    const clickedGenres = Object.keys(toggledItems);
    let _sortedGenres = [...genres];
    for (let i = 0; i < clickedGenres.length; i++) {
      if (toggledItems[clickedGenres[i]]) {
        _sortedGenres = _sortedGenres.filter((item) => item !== clickedGenres[i]);
        _sortedGenres = [clickedGenres[i], ..._sortedGenres];
      }
    }
    setSortedGenres(_sortedGenres);
  }, [toggledItems]);

  const handleToggle = (item) => {
    handleToggleGenre(item, userName, toggledItems, setToggledItems)
  };

  return (
    <div className="genredropdown-container">
      <button
        className="genredropdown-button"
        onClick={() => setIsDropdownVisible(!isDropdownVisible)}
      >
        Genres
      </button>

      {isDropdownVisible && (
        <div className="genredropdown-menu">
          {columns.map((column, colIndex) => (
            <div key={colIndex} className="genredropdown-column">
              {column.map((genre) => (
                <GenreButton
                  key={genre}
                  genre={genre}
                  isToggled={toggledItems[genre]}
                  onToggle={handleToggle}
                />
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default GenreDropdown;
