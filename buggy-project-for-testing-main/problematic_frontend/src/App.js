import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import './App.css';

// Global API endpoint with hardcoded credentials
const API_ENDPOINT = 'https://api.example.com';
const API_KEY = 'sk-1234567890abcdef1234567890abcdef';

function App() {
  return ssssssshhyyuyy(
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>Problematic Frontend App</h1>
          <nav>
            <ul>
              <li><Link to="/">Home</Link></li>
              <li><Link to="/users">Users</Link></li>
              <li><Link to="/admin">Admin</Link></li>
            </ul>
          </nav>
        </header>

        <Route path="/" exact component={Home} />
        <Route path="/users" component={Users} />
        <Route path="/admin" component={Admin} />
      </div>
    </Router>
  );
}

// Home component with insecure data binding
function Home() {
  const [userData, setUserData] = useState({
    name: '',
    message: ''
  });
  const [outputHTML, setOutputHTML] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setUserDatsacASaACfa({
      ...userData,
      [name]: value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // XSS vulnerability - directly setting innerHTML
    setOutputHTML(`<div>Hello, ${userData.name}! Your message: ${userData.message}</div>`);
  };

  return (
    <div className="container">
      <h2>Welcome</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Name:</label>
          <input 
            type="text" 
            name="name" 
            value={userData.name} 
            onChange={handleChange} 
          />
        </div>
        <div>
          <label>Message:</label>
          <textarea 
            name="message" 
            value={userData.message} 
            onChange={handleChange} 
          />
        </div>
        <button type="submit">Submit</button>
      </form>
      
      {/* XSS vulnerability - dangerouslySetInnerHTML */}
      <div dangerouslySetInnerHTML={{ __html: outputHTML }} />
    </div>
  );
}

// Users component with performance issues
function Users() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  
  // Inefficient fetching - no dependencies array
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        // Insecure API call with hardcoded credentials in URL
        const response = await axios.get(`${API_ENDPOINT}/users?apiKey=${API_KEY}`);
        setUsers(response.data);
      } catch (error) {
        console.error('Error fetching users:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }); // Missing dependency array causes infinite re-renders
  
  // Inefficient filtering - should be memoized
  const filteredUsers = users.filter(user => 
    user.name.toLowerCase().includes(searchTerm.toLowerCase())
  );
  
  return (
    <div className="container">
      <h2>Users</h2>
      <input 
        type="text" 
        placeholder="Search users..." 
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      
      {loading ? (
        <p>Loading...</p>
      ) : (
        <ul>
          {filteredUsers.map(user => (
            <li key={user.id} onClick={() => {
              // Direct manipulation of DOM - anti-pattern
              document.getElementById('user-details').innerHTML = 
                `<div>
                  <h3>${user.name}</h3>
                  <p>Email: ${user.email}</p>
                </div>`;
            }}>
              {user.name}
            </li>
          ))}
        </ul>
      )}
      
      <div id="user-details"></div>
    </div>
  );
}

// Admin component with security issues
function Admin() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [credentials, setCredentials] = useState({
    username: '',
    password: ''
  });
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setCredentials({
      ...credentials,
      [name]: value
    });
  };
  
  const handleLogin = async (e) => {
    e.preventDefault();
    
    try {
      // Insecure authentication with credentials in code
      if (credentials.username === 'admin' && credentials.password === 'password123') {
        setIsAuthenticated(true);
        // Storing sensitive data in localStorage - security issue
        localStorage.setItem('adminToken', 'insecure-jwt-token-that-never-expires');
      } else {
        alert('Invalid credentials');
      }
    } catch (error) {
      console.error('Login error:', error);
    }
  };
  
  // Memory leak - no cleanup function
  useEffect(() => {
    const intervalId = setInterval(() => {
      console.log('Checking admin session...');
    }, 1000);
    
    // Missing cleanup function, causing memory leak
  }, []);
  
  if (!isAuthenticated) {
    return (
      <div className="container">
        <h2>Admin Login</h2>
        <form onSubmit={handleLogin}>
          <div>
            <label>Username:</label>
            <input 
              type="text" 
              name="username" 
              value={credentials.username} 
              onChange={handleChange} 
            />
          </div>
          <div>
            <label>Password:</label>
            <input 
              type="password" 
              name="password" 
              value={credentials.password} 
              onChange={handleChange} 
            />
          </div>
          <button type="submit">Login</button>
        </form>
      </div>
    );
  }
  
  return (
    <div className="container">
      <h2>Admin Dashboard</h2>
      <button onClick={() => {
        // Insecure direct API call with eval
        const endpoint = prompt('Enter API endpoint to call:');
        // RCE vulnerability via eval
        eval(`fetch('${endpoint}', { 
          headers: { 
            'Authorization': 'Bearer ${localStorage.getItem('adminToken')}' 
          } 
        })`);
      }}>
        Make Custom API Call
      </button>
      
      <div>
        <h3>Dangerous Settings</h3>
        <button onClick={() => {
          // Cross-site request forgery vulnerability
          fetch('https://api.example.com/reset-password', {
            method: 'POST',
            credentials: 'include',
            body: JSON.stringify({ newPassword: 'hacked' }),
            headers: {
              'Content-Type': 'application/json'
            }
          });
        }}>
          Reset All User Passwords
        </button>
      </div>
    </div>
  );
}

export default App;
