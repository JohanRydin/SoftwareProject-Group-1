import React from 'react';
import './App.css';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="categories">
        <ul>
          <li><a href="https://test.com/action">Action</a></li>
          <li><a href="https://test.com/adventure">Adventure</a></li>
          <li><a href="https://test.com/racing">Racing</a></li>
          <li><a href="https://test.com/something">Something</a></li>
          <li><a href="https://test.com/something-else">Something Else</a></li>
        </ul>
      </div>
      <div className="search_bar">
        <input type="text" placeholder="Search..." />
      </div>
    </nav>
  );
}

export default Navbar;