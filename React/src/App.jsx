import React, { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './user/Navbar';
import Home from './user/Home';
import MyList from './user/MyList';
import Wishlist from './user/Wishlist';
import './App.css';

function App() {
  const [searchQuery, setSearchQuery] = useState('');


  return (
    <BrowserRouter>
      <div className="App">
        <Navbar setSearchQuery={setSearchQuery}/>
        <Routes>
          <Route path="/" element={<Home searchQuery={searchQuery} />} />
          <Route path="/mylist" element={<MyList />} />
          <Route path="/wishlist" element={<Wishlist />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;