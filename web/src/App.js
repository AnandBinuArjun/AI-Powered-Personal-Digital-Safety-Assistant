import React, { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard';
import Login from './components/Login';
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Check if user is already logged in (from localStorage or session)
    const token = localStorage.getItem('token');
    if (token) {
      // In a real app, you would verify the token with the backend
      setIsLoggedIn(true);
      // Set user data from token or API call
      setUser({ name: 'User' });
    }
  }, []);

  const handleLogin = (userData) => {
    setIsLoggedIn(true);
    setUser(userData);
    // Store token in localStorage
    localStorage.setItem('token', userData.token);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUser(null);
    // Remove token from localStorage
    localStorage.removeItem('token');
  };

  return (
    <div className="App">
      {isLoggedIn ? (
        <Dashboard user={user} onLogout={handleLogout} />
      ) : (
        <Login onLogin={handleLogin} />
      )}
    </div>
  );
}

export default App;