import React, { useState } from 'react';
import '../../App.css';
import './Login.css';

const LogIn = () => {
  //Defines 3 variables: email, password and login successful
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loginSuccessful, setLoginSuccessful] = useState(true);

  //handle submit function is called when the user submits the login form
  //sends a POST request to the backend server running on port 5000
  //with the email and password values as JSON objects
  const handleSubmit = async (event) => {
    event.preventDefault();
    const response = await fetch('http://127.0.0.1:5000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });

    //waits for a response from the server which comes in a message form
    //could be 'login successful' or 'login failed'
    const data = await response.json();
    console.log(data);

    if (data.message === 'Login successful') {
      setLoginSuccessful(true);
      window.location.href = '/profile'; //redirect to profiles page
    } else {
      setLoginSuccessful(false);
      setPassword('');
    }
  };

  //form in html formal with two input fields for email and password
  //the onsubmit handler is set to the handleSubmit function above
  //if login successful is false a message in red is rendered
  return (
    <div>
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
          />
        </div>
        <div>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </div>
        {loginSuccessful ? null : (
          <p style={{ color: 'red' }}>Incorrect credentials. Please try again.</p>
        )}
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default LogIn;
