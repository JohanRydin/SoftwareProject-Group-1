import React from 'react';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import './GenreDropdown';

const GenreButton = ({ genre, isToggled, onToggle }) => {
  return (
    <div
      className={`genredropdown-item ${isToggled ? "toggled-on" : ""}`} // Add extra css if toggled
      onClick={() => onToggle(genre)}
    >
      {genre}
      <svg>{isToggled && <ThumbUpIcon />}</svg>
    </div>
  );
};

export default GenreButton;
