import React from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Box, Typography, IconButton } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import DiceRolls from './DiceRolls';

const DiceRollsPopup = ({ open, onClose, rollsConfig, onRerollAll }) => {
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
            Dice Rolls
          </Typography>
          <IconButton
            aria-label="close"
            onClick={onClose}
            style={{ position: 'absolute', right: '8px', top: '8px' }}
          >
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent style={{ flex: 1, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <DiceRolls rollsConfig={rollsConfig} />
        </DialogContent>
        <DialogActions style={{ justifyContent: 'space-between', padding: '16px' }}>
          <Button onClick={onRerollAll} color="secondary" variant="contained">
            Reroll All
          </Button>
          <Button onClick={() => {}} color="primary" variant="contained">
            Submit
          </Button>
        </DialogActions>
      </Box>
    </Dialog>
  );
};

export default DiceRollsPopup;
