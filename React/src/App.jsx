import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './user/Navbar';
import Home from './user/Home';
import MyList from './user/MyList';
import Wishlist from './user/Wishlist';
import './App.css';
import LoginModal from './user/LoginModal.jsx'
import { GenreProvider} from "./user/GenreProvider.jsx";
import { useCookies } from 'react-cookie';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [displayMyList, setDisplayMyList] = useState(false); 
  const [displayWishlist, setDisplayWishlist] = useState(false); 
  const [userName, setUser] = useState(null);
  const [userID, setUserID] = useState(-1);
  const [loginModalOpen, setLoginModalOpen] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false); 
  const [refreshKey, setRefreshKey] = useState(0);
  //cookies['user'] for logged in user, doesnt exist if not previously logged in
  //cookies['userID'] for id of the logged in user
  const [cookies, setCookie, removeCookie] = useCookies(['cookie-name']);
 
  useEffect(()=>{
    //load cookie and log in
    const cookieUser = cookies['user']
    const cookieID = cookies['userID']
    if(cookieUser && cookieID ){
      setUser(cookieUser);
      setUserID(cookieID);
      setIsLoggedIn(true)
      //how do i fix this?
      //setGenresPrefs(userName, setLikedGenres);
    }
  }, [])

  const forceUpdate = () => {
    setDisplayMyList(false);
    setDisplayWishlist(false);
    setSearchQuery('')
    setRefreshKey(refreshKey + 1)

  };


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
        cookieSet={setCookie}

      />}

        <div className="App">
          <Navbar setSearchQuery={setSearchQuery} displayMyList={displayMyList} setDisplayMyList={setDisplayMyList} displayWishlist={displayWishlist} setDisplayWishlist={setDisplayWishlist}
          userName={userName} setUser={setUser} loginModalOpen={loginModalOpen} setLoginModalOpen={setLoginModalOpen} isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} refresh={forceUpdate} 
          removeCookie={removeCookie}/>
          <Routes>
            <Route path="/" element={<Home searchQuery={searchQuery} displayMyList={displayMyList} displayWishlist={displayWishlist} userName={userName} refreshState={refreshKey}/>} />
            <Route path="/mylist" element={<MyList />} />
            <Route path="/wishlist" element={<Wishlist />} />
          </Routes>
        </div>
      </BrowserRouter>
    </GenreProvider>
  );
}

export default App;