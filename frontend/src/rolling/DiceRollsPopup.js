import React, { useState } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Box, Typography, IconButton, TextField, Grid } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import DiceRolls from './DiceRolls';
import MultiSelectComponent from './MultiSelectComponent';

const DiceRollsPopup = ({ open, onClose, rollsModal, onRerollAll }) => {
  const backendUrl = process.env.REACT_APP_BACKEND_URL;
  const [level, setLevel] = useState(null);
  const [selections, setSelections] = useState([]);
  const [diceResults, setDiceResults] = useState([]);

  const handleRollResult = (diceType, rollResult) => {
    setDiceResults((prevResults) => ({
      ...prevResults,
      [diceType]: rollResult,
    }));
  };

  const handleSubmit = async () => {
    // Gather all necessary data
    const selectedLevel = level;
    // Assuming MultiSelectComponent and DiceRolls have methods to get their current state
    // const selections = /* Get selections from MultiSelectComponent */;
    const diceRolls = diceResults;

    // Data to be sent in the POST request
    const submitData = {
      level: selectedLevel,
      selection: selections,
      rolls: diceRolls,
    };

    try {
      const response = await fetch(backendUrl + "/guns/guns_roll", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(submitData),
      });

      if (response.ok) {
        const result = await response.json();
        console.log('Submit successful:', result);
        onClose();

      } else {
        console.error('Submit failed:', response.statusText);
      }
    } catch (error) {
      console.error('Error during submit:', error);

    }
  };
  return (
    <Dialog
      open={open}
      onClose={onClose}
      fullWidth
      maxWidth="lg"
      PaperProps={{
        style: {
          width: '80%',
          height: '80%',
        },
      }}
    >
      <Box display="flex" flexDirection="column" height="100%">
        <DialogTitle style={{ textAlign: 'center', position: 'relative' }}>
          <Typography variant="h4" component="div" style={{ fontWeight: 'bold' }}>
            {rollsModal.label}
          </Typography>
        </DialogTitle>
        {/* Note this icon button needs to be below the first title otherwise you cant click it grr */}
        <IconButton
          aria-label="close"
          onClick={onClose}
          style={{ position: 'absolute', right: '8px', top: '8px' }}
        >
          <CloseIcon />
        </IconButton>
        {rollsModal.level &&
          <>
            <DialogTitle style={{ textAlign: 'center', position: 'relative' }}>
              <Typography variant="h4" component="div" style={{ fontWeight: 'bold' }}>
                Level choice
              </Typography>
            </DialogTitle>
            <Grid container style={{ justifyContent: 'center', alignItems: 'center' }}>
              <Grid item>
                <Typography variant="body1">Level:</Typography>
              </Grid>
              <Grid item>
                <TextField
                  type="number"
                  value={level}
                  onChange={(e) => {
                    const newLevel = parseInt(e.target.value) || 0;
                    setLevel(newLevel);
                  }}
                  fullWidth
                  variant="outlined"
                />
              </Grid>
            </Grid>
          </>
        }
        {rollsModal.selections !== null && rollsModal.selections.mandatory !== null && rollsModal.selections.mandatory.length > 0 &&
          <>
            <DialogTitle style={{ textAlign: 'center', position: 'relative' }}>
              <Typography variant="h4" component="div" style={{ fontWeight: 'bold' }}>
                Selections
              </Typography>
            </DialogTitle>
            <DialogContent style={{ justifyContent: 'center', alignItems: 'center' }}>
              <MultiSelectComponent selectionData={rollsModal.selections.mandatory} onSelectionChange={setSelections} />
            </DialogContent>
          </>
        }
        <DialogTitle style={{ textAlign: 'center', position: 'relative' }}>
          <Typography variant="h4" component="div" style={{ fontWeight: 'bold' }}>
            Dice Rolls
          </Typography>
        </DialogTitle>
        <DialogContent style={{ justifyContent: 'center', alignItems: 'center' }}>
          <DiceRolls rollsConfig={rollsModal.rolls} onRollResults={handleRollResult} />
        </DialogContent>
        <DialogActions style={{ justifyContent: 'space-between', padding: '16px' }}>
          <Button onClick={onRerollAll} color="secondary" variant="contained">
            Reroll All
          </Button>
          <Button onClick={handleSubmit} color="primary" variant="contained">
            Submit
          </Button>
        </DialogActions>
      </Box>
    </Dialog >
  );
};

export default DiceRollsPopup;
