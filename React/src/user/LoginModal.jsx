import React, { useState, useEffect } from 'react';
import './LoginModal.css';
import { getUser, newUser } from './Connections.jsx'
import { useGenreContext, setGenresPrefs } from './GenreProvider.jsx';

export const LoginModal = ({ onClose, setIsLoggedIn, setUser, setUserID, setLoginModalOpen }) => {
  const [inputValue, setInputValue] = useState('');
  const [inputValuePassword, setInputValuePassword] = useState('');
  const [inputError, setInputError] = useState(false);
  const [registerError, setRegisterError] = useState(false)
  const { setLikedGenres } = useGenreContext();

  const handleLogin = (e) => {
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
        setInputError(true)
      });  // Display error if login failed
  };

  const handleRegister = (e) => {
    e.preventDefault();

    const username = inputValue
    newUser(username).then(data => {
      console.log(data)

      setIsLoggedIn(true)
      setUserID(data['userID'])
      setUser(data['username'])

      setLoginModalOpen(false)  // Close modal
    }).catch(
      e => {
        console.log("Error creating user:", e)
        setRegisterError(true)
      });  // Display error if login failed
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
        <div className='buttonsDiv'>
          <button type="submit" className="login-button login-margin" onClick={handleLogin}>Login</button>
          <button className="login-button" onClick={handleRegister}>Register</button>
        </div>
        {registerError && <p className="login-error login-margin">Username already taken.</p>}
      </div>
    </div>
  );
};

export default LoginModal;
