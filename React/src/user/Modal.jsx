import starIcon from './star-icon.svg';  


export const Modal = ({ isOpen, onClose, game }) => {
    if (!isOpen) return null;
  
    return (
      <div className="modal-overlay" onClick={onClose}>
        <div className="modal-content" onClick={e => e.stopPropagation()}>
          <button className="close-button" onClick={onClose}>×</button>
          <h2 className="modal-title">{game["gamename"]}</h2>
          <hr className="modal-divider" />
          <p className="modal-ranking">
            Rating: {0} <img src={starIcon} alt="Star Icon" className="star-icon" />
          </p>
          <p className="modal-genres">Genres: {game["genres"]}</p>
          <p className="modal-description">{game["description"]}</p>
        </div>
      </div>
    );
  };
  
export default Modal;
