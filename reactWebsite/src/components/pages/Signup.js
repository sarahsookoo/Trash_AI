import React, { useState } from 'react';
import { Button } from '../Button';
// import '../../App.css';
import './Signup.css';

const Signup = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    const response = await fetch('http://127.0.0.1:5000/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ name, email, password })
    });
    const data = await response.json();
    console.log(data);
  };

  return (
    
    <div className='signup'>
      <h1>Sign-Up</h1>
      <div className='signup-container'>
      <form onSubmit={handleSubmit}>
        <div className='name-container'>
          <label htmlFor="name">Name: </label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(event) => setName(event.target.value)}
          />
        </div>
        <div className='email-container'>
          <label htmlFor="email">Email: </label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
          />
        </div>
        <div className='password-container'>
          <label htmlFor="password">Password: </label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </div>
        {/* <button type="submit">Signup</button> */}
        <div className='signup-btn'>
                <Button 
                className='btns' 
                button type="submit"
                buttonStyle='btn--page'
                buttonSize='btn--large'>
                    Sign-Up
                </Button>
        </div>
      </form>
      </div>
    </div>
  );
};

export default Signup;
