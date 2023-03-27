import React from 'react';
import NavBar from './components/NavBar';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Home from './components/pages/Home';
import Services from './components/pages/Services';
import Profile from './components/pages/Profile';
import LogIn from './components/pages/LogIn';

function App() {
  return (
    <>
    <Router>
      <NavBar />
      <Routes>
        {/* <Route path='/' exact component={Home} /> */}

        <Route exact path='/' element={<Home />}>
        <Route exact path='/services' element={<Services />}></Route>
        <Route exact path='/profile' element={<Profile />}></Route>
        <Route exact path='/log-in' element={<LogIn />}></Route>
        </Route>

        {/* <Route exact path="/" element={<Home />} />
        <Route exact path="/services" element={<Services />} />
        <Route exact path="/profile" element={<Profile />} />
        <Route exact path="/log-in" element={<LogIn />} /> */}

        {/* <Route path="/" element={<Home />} />
        <Route path="/services" element={<Services />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/log-in" element={<LogIn />} /> */}

        {/* <Route exact path="/" element={<Home />}>
        <Route exact path="/services" element={<Services />}>
        <Route exact path="/profile" element={<Profile />}>
        <Route exact path="/log-in" element={<LogIn />}>
        </Route> */}
        

      </Routes>
    </Router>
    </>
  );
}

export default App;
