import React, { useState, useEffect } from 'react';
import './LoginModal.css';
import { getUser } from './Connections.jsx'
import { useGenreContext, setGenresPrefs } from './GenreProvider.jsx';

export const LoginModal = ({ onClose, setIsLoggedIn, setUser, setUserID, setLoginModalOpen}) => {
  const [inputValue, setInputValue] = useState('');
  const [inputValuePassword, setInputValuePassword] = useState('');
  const [inputError, setInputError] = useState(false);
  const { setLikedGenres } = useGenreContext();
  
  const handleSubmit = (e) => {
    e.preventDefault();
    
    const name = inputValue
    getUser(name).then(data => {

      setIsLoggedIn(true);  // Set user info in system
      setUserID(data['userID'])
      setUser(data['username'])
      setGenresPrefs(name, setLikedGenres);

      setLoginModalOpen(false)  // Close modal
    }).catch(
      e => {
      console.log("Error fetching user:", e)
      setInputError(true)});  // Display error if login failed
  };

  const onChangeUsername = (e) => {
    setInputValue(e.target.value)
  }
  const onChangePassword = (e) => {
    setInputValuePassword(e.target.value)
  }

    return (
      <div className="login-modal-overlay" onClick={onClose}>
        <div className="login-modal-content" onClick={e => e.stopPropagation()}>
          <form onSubmit={handleSubmit} className="login-form">
          <input
            type="text"
            placeholder="Username..."
            value={inputValue}
            onChange={onChangeUsername}
            className="login-input login-margin"
          />
          <input
          type="text"
          placeholder="Password..."
          value={'*'.repeat(inputValuePassword.length)}
          onChange={onChangePassword}
          className="login-input login-margin"
        />
          {inputError && <p className="login-error login-margin">Login failed, try again.</p>}
          <button type="submit" className="login-button login-margin">Login</button>
          <button className="login-button">Register</button>
        </form>
        </div>
      </div>
    );
  };
  
export default LoginModal;
