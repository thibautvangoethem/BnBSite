import React, { useState } from 'react';
import { TextField, Button, Container, Typography, Paper, Alert} from '@mui/material';
import { useAuth } from './AuthContext';

const Login = () => {
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const { setBearerToken } = useAuth();

  const backendUrl = process.env.REACT_APP_BACKEND_URL;

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(''); // Clear any previous errors
    setSuccess(false); // Clear any previous success messages

    try {
        // Create form-encoded data
        const formData = new URLSearchParams();
        formData.append("grant_type", "password");
        formData.append("username", name);
        // formData.append("password", "password");
        formData.append("password", "niet echt relevant");
        formData.append("scope", ""); 

        const response = await fetch(backendUrl + "/token", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded", // Correct Content-Type for form encoding
            },
            body: formData.toString(), // Send form-encoded data as body
        });

        if (!response.ok) {
            throw new Error("Login failed. Please check your credentials.");
        }

        const data = await response.json();

        if (data.access_token) {
            localStorage.setItem("bearerToken", data.access_token); // Save token in localStorage
            setBearerToken(data.access_token); // Update the writable store (optional)
            console.log("Login successful. Token saved:", data.access_token);
            setSuccess(true);
        } else {
            const errorData = await response.json();    
            setError(errorData.detail || 'Login failed');
            setBearerToken("");
        }
    } catch (err) {
        setError('An error occurred. Please try again.');
        console.error('Error during login:', err);
        setBearerToken("");
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <Paper elevation={3} style={{ padding: '20px', marginTop: '50px' }}>
        <Typography component="h1" variant="h5">
          Sign in
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="name"
            label="Papier hier (of naam)"
            name="name"
            autoComplete="name"
            autoFocus
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          {/* <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          /> */}
           {error && <Alert severity="error">{error}</Alert>}
           {success && <Alert severity="success">Login successful!</Alert>}
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            style={{ marginTop: '20px' }}
          >
            Sign In
          </Button>
        </form>
      </Paper>
    </Container>
  );
};

export default Login;
