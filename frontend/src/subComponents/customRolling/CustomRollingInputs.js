import React, { useState } from 'react';
import { TextField, Typography, Grid, Box, Button, Paper, FormControl } from '@mui/material';
import { DiceEnum } from '../../rolling/DiceEnum';
import { v4 as uuidv4 } from 'uuid';

const CustomRollingInputs = ({ onSerialize }) => {
  // Generate labels dynamically from DiceEnum keys
  const labels = Object.keys(DiceEnum);
  const [values, setValues] = useState(Array(labels.length).fill(0));

  const handleSerialize = () => {
    // Create the entries array with optional labels
    const entries = labels.map((label, index) => {
      const diceArray = Array(values[index]).fill(label);
      return {
        diceList: diceArray,
        ...(label && { label }), // Include label only if it exists
      };
    });

    // Create the rollsConfig object
    const rollsConfig = {
      uuid: uuidv4(),
      entries,
    };

    const rollmodal = {
      level: false,
      selections: {
        mandatory: [],
        optional: [],
      },
      rolls: rollsConfig
    }

    // Call the onSerialize function with the rollsConfig
    onSerialize(rollmodal);
  };
  const handleWheel = (e, index) => {
    e.preventDefault();
    const newValues = [...values];
    if (e.deltaY < 0) {
      newValues[index] = values[index] + 1;
    } else {
      newValues[index] = Math.max(0, values[index] - 1);
    }
    setValues(newValues);
  };

  return (
    <Box p={2}>
      <Paper elevation={3} p={2}>
        <Box p={2}>
          <Typography variant="h4" gutterBottom>Hoeveel rolls van welke dice?</Typography>
          {labels.map((label, index) => (
            <Grid container alignItems="center" spacing={2} key={index} mb={2}>
              <Grid item>
                <Typography variant="body1">{label}</Typography>
              </Grid>
              <Grid item>
                <FormControl fullWidth>
                  <TextField
                    type="number"
                    value={values[index]}
                    onChange={(e) => {
                      const newValues = [...values];
                      newValues[index] = e.target.value === '' ? 0 : parseInt(e.target.value) || 0;
                      setValues(newValues);
                    }}
                    onWheel={(e) => handleWheel(e, index)}
                    fullWidth
                    variant="outlined"
                  />
                </FormControl>
              </Grid>
            </Grid>
          ))}
          <Box mt={2}>
            <Button variant="contained" color="primary" onClick={handleSerialize}>
              ROLL ROLL ROLL!
            </Button>
          </Box>
        </Box>
      </Paper>
    </Box>
  );
};

export default CustomRollingInputs;