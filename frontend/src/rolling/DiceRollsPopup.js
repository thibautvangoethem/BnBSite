import React, { useState } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Box, Typography, IconButton, TextField, Grid } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import DiceRolls from './DiceRolls';
import MultiSelectComponent from './MultiSelectComponent';

const DiceRollsPopup = ({ open, onClose, rollsModal, onRerollAll }) => {
  const [level, setLevel] = useState(null);
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
              <MultiSelectComponent selectionData={rollsModal.selections.mandatory} />
            </DialogContent>
          </>
        }
        <DialogTitle style={{ textAlign: 'center', position: 'relative' }}>
          <Typography variant="h4" component="div" style={{ fontWeight: 'bold' }}>
            Dice Rolls
          </Typography>
        </DialogTitle>
        <DialogContent style={{ justifyContent: 'center', alignItems: 'center' }}>
          <DiceRolls rollsConfig={rollsModal.rolls} />
        </DialogContent>
        <DialogActions style={{ justifyContent: 'space-between', padding: '16px' }}>
          <Button onClick={onRerollAll} color="secondary" variant="contained">
            Reroll All
          </Button>
          <Button onClick={() => { }} color="primary" variant="contained">
            Submit
          </Button>
        </DialogActions>
      </Box>
    </Dialog >
  );
};

export default DiceRollsPopup;
