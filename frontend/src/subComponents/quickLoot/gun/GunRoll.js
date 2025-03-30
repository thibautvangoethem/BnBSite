import React, { useEffect, useState } from 'react';
import { Box, Button, FormControl, InputLabel, Select, MenuItem } from '@mui/material';

const GunRoll = () => {
  const backendUrl = process.env.REACT_APP_BACKEND_URL;
  const [data, setData] = useState(null);
  const [selections, setSelections] = useState({});

  useEffect(() => {
    // Fetch data from the backend
    const fetchData = async () => {
      try {
        const response = await fetch(backendUrl+'/gun/options')
        const result = await response.json();
        setData(result);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const handleChange = (label, value) => {
    setSelections((prevSelections) => ({
      ...prevSelections,
      [label]: value,
    }));
  };

  const handleRoll = () => {
    // Implement the roll logic here
    console.log('Selections:', selections);
  };

  if (!data) {
    return <Box>Loading...</Box>;
  }

  return (
    <Box
      sx={{
        border: '2px solid #ccc',
        borderRadius: '8px',
        padding: '16px',
        width: '100%',
        boxSizing: 'border-box',
        boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.1)',
        display: 'flex',
        flexDirection: 'column',
        gap: '16px',
      }}
    >
      {Object.entries(data).map(([label, options]) => (
        <FormControl key={label} fullWidth>
          <InputLabel>{label}</InputLabel>
          <Select
            value={selections[label] || ''}
            label={label}
            onChange={(event) => handleChange(label, event.target.value)}
          >
            {options.map((option) => (
              <MenuItem key={option} value={option}>
                {option}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      ))}
      <Button variant="contained" color="primary" onClick={handleRoll}>
        ROLL
      </Button>
    </Box>
  );
};

export default GunRoll;
