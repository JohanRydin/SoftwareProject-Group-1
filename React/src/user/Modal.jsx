import React from 'react';
import './Modal.css';
import starIcon from './star-icon.svg';
import GenreButton from './GenreButton';


export const Modal = ({ isOpen, onClose, game }) => {
  if (!isOpen) return null;

  // game.genres is a string looking like "['action', 'rpg'...]". Can be parsed as list but we need to replace ' with " first
  const genres = JSON.parse(game.genres.replace(/'/g, '"'));

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <button className="close-button" onClick={onClose}>×</button>
        <h2 className="modal-title">{game["gamename"]}</h2>
        <hr className="modal-divider" />
        <img src={game.image} alt={game.gamename} className="modal-image" />
        <hr className="modal-divider" />
        <p className="modal-description">{game["description"]}</p>
        <div className="modal-genres">
          <div className="genres-list">
            {genres.map((genre) => (
              <GenreButton
                key={genre}
                genre={genre}
                isToggled={false}
                onToggle={() => {}}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Modal;
