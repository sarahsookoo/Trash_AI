import React from 'react';
import NavBar from './components/NavBar';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Home from './components/pages/Home';
import Services from './components/pages/Services';
import Profile from './components/pages/Profile';
import LogIn from './components/pages/LogIn';
import Signup from './components/pages/Signup';

function App() {
  return (
    <>
    <Router>
      <NavBar />
      <Routes>

          <Route path='/' element={<Home />} />
          <Route path='/home' element={<Home />} />
          <Route path='/services' element={<Services />} />
          <Route path='/profile' element={<Profile />} />
          <Route path='/signup' element={<Signup />} />
          <Route path='/login' element={<LogIn />} />
        
      </Routes>
    </Router>
    </>
  );
}

export default App;