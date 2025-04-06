import React, { useEffect, useState } from 'react';
import { Typography, Grid } from '@mui/material';
import { DiceEnum } from './DiceEnum';

const DiceRoller = ({ diceType, onRollResult }) => {
  const [result, setResult] = useState(null);

  useEffect(() => {
    const rollDice = () => {
      const sides = DiceEnum[diceType];
      if (sides) {
        const roll = Math.floor(Math.random() * sides) + 1;
        setResult(roll);
        console.log(`Rolled a ${diceType}-sided die: ${roll}`); // Debugging log

        onRollResult(roll);
      } else {
        console.error('Invalid dice type:', diceType);
      }
    };

    rollDice();
  }, [diceType]);

  return (
    <Grid container alignItems="center" spacing={2}>
      <Grid item>
        <Typography variant="body1">{diceType}</Typography>
      </Grid>
      <Grid item>
        {result !== null && (
          <Typography variant="h6">{result}</Typography>
        )}
      </Grid>
    </Grid>
  );
};

export default DiceRoller;
