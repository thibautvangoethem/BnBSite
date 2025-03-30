import React, { useState } from 'react';
import { TextField, Typography, Grid, Box, Button } from '@mui/material';

const CustomRollingInputs = ({ onSerialize }) => {
  const labels = ["D2", "D4", "D6", "D8", "D10", "D12", "D20", "D100"];
  const [values, setValues] = useState(Array(labels.length).fill(0));

  const handleSerialize = () => {
    const serializedData = labels.map((label, index) => ({
      [label]: values[index],
    }));

    // Convert the array of objects into a single object
    const rollsConfig = serializedData.reduce((acc, curr) => ({ ...acc, ...curr }), {});

    // Call the onSerialize function with the rollsConfig
    onSerialize(rollsConfig);
  };

  return (
    <Box>
      <h1>Hoeveel rolls van welke dice?</h1>
      {labels.map((label, index) => (
        <Grid container alignItems="center" spacing={2} key={index} mb={2}>
          <Grid item>
            <Typography variant="body1">{label}</Typography>
          </Grid>
          <Grid item>
            <TextField
              type="number"
              value={values[index]}
              onChange={(e) => {
                const newValues = [...values];
                newValues[index] = parseInt(e.target.value) || 0;
                setValues(newValues);
              }}
              fullWidth
              variant="outlined"
              inputProps={{ min: 0, step: 1 }}
            />
          </Grid>
        </Grid>
      ))}
      <Button variant="contained" color="primary" onClick={handleSerialize}>
        ROLL ROLL ROLL!
      </Button>
    </Box>
  );
};

export default CustomRollingInputs;
