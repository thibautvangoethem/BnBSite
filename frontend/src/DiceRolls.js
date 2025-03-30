import React from 'react';
import { Box } from '@mui/material';
import DiceRoller from './DiceRoller';

const DiceRolls = ({ rollsConfig }) => {
  return (
    <Box
      sx={{
        border: '2px solid #ccc',
        borderRadius: '8px',
        padding: '32px', // Increased padding to take up more space
        width: '100%', // Ensure it takes up full width
        height: '100%', // Ensure it takes up full height
        boxSizing: 'border-box', // Include padding and border in the element's total width and height
        boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.1)',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      {Object.entries(rollsConfig).map(([diceType, count]) => (
        <Box key={diceType} mb={2} width="100%">
          {Array.from({ length: count }, (_, index) => (
            <DiceRoller key={index} diceType={diceType} />
          ))}
        </Box>
      ))}
    </Box>
  );
};

export default DiceRolls;
