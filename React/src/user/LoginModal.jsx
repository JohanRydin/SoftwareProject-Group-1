import React, { useState } from 'react';
import './LoginModal.css';
import { getUser } from './Connections.jsx'

export const LoginModal = ({ onClose, setIsLoggedIn, setUser, setUserID, setLoginModalOpen}) => {
  const [inputValue, setInputValue] = useState('');
  const [inputValuePassword, setInputValuePassword] = useState('');
  const [inputError, setInputError] = useState(false);
  
  const handleSubmit = (e) => {
    e.preventDefault();
    
    const name = inputValue
    getUser(name).then(data => {
      console.log(data);

      setIsLoggedIn(true);  // Set user info in system
      setUserID(data['userID'])
      setUser(data['username'])

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
      <div className="modal-overlay" onClick={onClose}>
        <div className="modal-content" onClick={e => e.stopPropagation()}>
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
