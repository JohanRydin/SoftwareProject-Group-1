import React, { useState, useEffect } from "react";
import "./GenreDropdown.css";
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import { postGenrePreference, deleteGenrePreference } from './Connections.jsx'

const GenreDropdown = ({ genres, likedGenres, userName }) => {
  const [isDropdownVisible, setIsDropdownVisible] = useState(false);
  const [toggledItems, setToggledItems] = useState({});

  useEffect(() => {
    const initialToggled = {};
    likedGenres.forEach((genre) => {
      initialToggled[genre] = true;
    });
    setToggledItems(initialToggled);
  }, [likedGenres]);

  const columns = genres.reduce((result, genre, index) => {
    const columnIndex = index % 4;
    if (!result[columnIndex]) {
      result[columnIndex] = [];
    }
    result[columnIndex].push(genre);
    return result;
  }, []);

  const handleToggle = (item) => {
    if (userName != null) {
      if (toggledItems[item]) {
        try {
          deleteGenrePreference(userName, item)
        }
        catch (e) {
          console.log(e);
        }
      }
      else {
        try {
          postGenrePreference(userName, item)
        }
        catch (e) {
          console.log(e);
        }
      }
    }
    setToggledItems((prev) => ({
      ...prev,
      [item]: !prev[item],
    }));
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
              {column.map((item) => (
                <div
                  key={item}
                  className={`genredropdown-item ${
                    toggledItems[item] ? "toggled-on" : "" // Add extra css if toggled
                  }`}
                  onClick={() => handleToggle(item)}
                >
                  {item}
                  <svg>{toggledItems[item] && <ThumbUpIcon />}</svg>
                </div>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default GenreDropdown;
