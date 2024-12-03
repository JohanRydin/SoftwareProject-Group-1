import React, { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './user/Navbar';
import Home from './user/Home';
import MyList from './user/MyList';
import Wishlist from './user/Wishlist';
import './App.css';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [displayMyList, setDisplayMyList] = useState(false); 
  const [displayWishlist, setDisplayWishlist] = useState(false); 
  const [userName, setUser] = useState('Erik');


  return (
    <BrowserRouter>
      <div className="App">
        <Navbar setSearchQuery={setSearchQuery} displayMyList={displayMyList} setDisplayMyList={setDisplayMyList} displayWishlist={displayWishlist} setDisplayWishlist={setDisplayWishlist} setUser={setUser} />
        <Routes>
          <Route path="/" element={<Home searchQuery={searchQuery} displayMyList={displayMyList} displayWishlist={displayWishlist} userName={userName} />} />
          <Route path="/mylist" element={<MyList />} />
          <Route path="/wishlist" element={<Wishlist />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;