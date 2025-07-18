import React, { useState } from 'react';

import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Box, Typography, IconButton, TextField, Grid } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import DiceRolls from './DiceRolls';
import MultiSelectComponent from './MultiSelectComponent';
import { useNavigate } from "react-router";

const DiceRollsPopup = ({ open, onClose, rollsModal, onRerollAll }) => {
  const backendUrl = process.env.REACT_APP_BACKEND_URL;
  const navigate = useNavigate();
  const [level, setLevel] = useState(null);
  const [selectionsResults, setSelectionsResults] = useState([]);
  const [optionResults, setoptionResults] = useState([]);
  const [diceResults, setDiceResults] = useState([]);

  const handleRollResult = (label, index, rollResult) => {
    setDiceResults((prevResults) => {

      const newResults = { ...prevResults };
      if (!newResults[label]) {
        newResults[label] = [];
      }
      const resultsArray = [...newResults[label]];
      resultsArray[index] = rollResult;
      newResults[label] = resultsArray;

      return newResults;
    });
  };

  const handleSubmit = async () => {
    // Gather all necessary data
    const selectedLevel = level;
    // Assuming MultiSelectComponent and DiceRolls have methods to get their current state
    // const selections = Object.entries(selectionsResults).map(([label, choices]) =>
    // ({
    //   label: label,
    //   choices: choices
    // })
    // )
    const diceRolls = Object.entries(diceResults).map(([label, rolls]) => ({
      label: label,
      result: rolls
    }));

    const submitData = {
      level: !rollsModal.level ? 0 : selectedLevel,
      selections: selectionsResults,
      options: optionResults,
      rolls: diceRolls,
    };

    console.log('asfgfdasg');
    try {
      const response = await fetch(backendUrl + rollsModal.post, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(submitData),
      });

      if (response.ok) {
        const result = await response.json();
        console.log('Submit successful:', result);
        if (result.item_type === 'shield') {
          navigate(`/viz/shield/${result.item_id}`);
        } else if (result.item_type === 'gun') {
          navigate(`/viz/gun/${result.item_id}`);
        } else if (result.item_type === 'potion') {
          navigate(`/viz/potion/${result.item_id}`);
        } else if (result.item_type === 'grenade') {
          navigate(`/viz/grenade/${result.item_id}`);
        } else {
          console.warn(`unknown viz type ${result.item_type}`)
        }
        onClose(result);
      } else {
        console.error('Submit failed:', response.statusText);
      }
    } catch (error) {
      console.error('Error during submit:', error);
    }
  };
  return (
    <>
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
                <Typography variant="H1" component="div" style={{ fontWeight: 'bold' }}>
                  Selections
                </Typography>
              </DialogTitle>
              <DialogContent style={{ justifyContent: 'center', alignItems: 'center' }}>
                <MultiSelectComponent selectionData={rollsModal.selections.mandatory} onSelectionChange={setSelectionsResults} />
              </DialogContent>
            </>
          }
          {rollsModal.selections !== null && rollsModal.selections.optional !== null && rollsModal.selections.optional.length > 0 &&
            <>
              <DialogTitle style={{ textAlign: 'center', position: 'relative' }}>
                <Typography variant="H1" component="div" style={{ fontWeight: 'bold' }}>
                  Options
                </Typography>
              </DialogTitle>
              <DialogContent style={{ justifyContent: 'center', alignItems: 'center' }}>
                <MultiSelectComponent selectionData={rollsModal.selections.optional} onSelectionChange={setoptionResults} />
              </DialogContent>
            </>
          }
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
    </>
  );

};

export default DiceRollsPopup;
