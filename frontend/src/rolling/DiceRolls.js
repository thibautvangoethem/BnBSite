import React from 'react';
import { Box } from '@mui/material';
import DiceRoller from './DiceRoller'; // Assuming DiceRoller is a separate component

const DiceRolls = ({ rollsConfig, onRollResults }) => {
  if (!rollsConfig) {
    return <Box>rollsConfig is empty.</Box>;
  }
  if (!Array.isArray(rollsConfig.entries)) {
    return <Box>rollsConfig.entries is not an array.</Box>;
  }
  if (rollsConfig.entries.length === 0) {
    return <Box>rollsConfig.entries.length is empty.</Box>;
  }

  const handleRollResult = (label, index, rollResult) => {
    // Notify the parent component (DiceRollsPopup) about the roll result
    onRollResults(label, index, rollResult);
  };

  return (
    <Box
      sx={{
        border: '2px solid #ccc',
        borderRadius: '8px',
        padding: '16px',
        width: '100%',
        height: '100%',
        boxSizing: 'border-box',
        boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.1)',
        overflowY: 'auto',
        display: 'flex',
        flexDirection: 'column',
        gap: '16px',
      }}
    >
      {rollsConfig.entries.map((entry, typeIndex) => (
        <Box key={`${entry.label}-${rollsConfig.uuid}-${typeIndex}`} width="100%">
          {entry.label && (
            <Box sx={{ marginBottom: '8px', fontWeight: 'bold' }}>
              {entry.label}
            </Box>
          )}
          {entry.diceList.map((diceType, index) => (
            <Box
              key={`${diceType}-${rollsConfig.uuid}-${typeIndex}-${index}`}
              sx={{
                border: '1px solid #ddd',
                borderRadius: '4px',
                padding: '8px',
                width: '100%',
                boxSizing: 'border-box',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                marginBottom: '8px', // Add some space between dice boxes
              }}
            >
              <DiceRoller diceType={diceType} />
            </Box>
          ))}
        </Box>
      ))}
    </Box>
  );
};

export default DiceRolls;
