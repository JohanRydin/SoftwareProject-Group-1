import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

import Navbar from './Navbar';

function App() {
  return (
    <>
      <Navbar />
      <div className="content"></div>
    </>
  );
}

export default App;
