import React, { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './user/Navbar';
import Home from './user/Home';
import MyList from './user/MyList';
import Wishlist from './user/Wishlist';
import './App.css';
import LoginModal from './user/LoginModal.jsx'
import { GenreProvider } from "./user/GenreProvider.jsx";

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [displayMyList, setDisplayMyList] = useState(false); 
  const [displayWishlist, setDisplayWishlist] = useState(false); 
  const [userName, setUser] = useState(null);
  const [userID, setUserID] = useState(-1);
  const [loginModalOpen, setLoginModalOpen] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);  


  return (
    <GenreProvider>
      <BrowserRouter>
      {loginModalOpen &&
      <LoginModal 
        onClose={() => setLoginModalOpen(false)}
        setIsLoggedIn={setIsLoggedIn}
        setUser={setUser}
        setUserID={setUserID}
        setLoginModalOpen={setLoginModalOpen}
      />}

        <div className="App">
          <Navbar setSearchQuery={setSearchQuery} displayMyList={displayMyList} setDisplayMyList={setDisplayMyList} displayWishlist={displayWishlist} setDisplayWishlist={setDisplayWishlist}
          userName={userName} setUser={setUser} loginModalOpen={loginModalOpen} setLoginModalOpen={setLoginModalOpen} isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} />
          <Routes>
            <Route path="/" element={<Home searchQuery={searchQuery} displayMyList={displayMyList} displayWishlist={displayWishlist} userName={userName} />} />
            <Route path="/mylist" element={<MyList />} />
            <Route path="/wishlist" element={<Wishlist />} />
          </Routes>
        </div>
      </BrowserRouter>
    </GenreProvider>
  );
}

export default App;