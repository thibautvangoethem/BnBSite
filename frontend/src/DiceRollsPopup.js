import React from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Box, Typography } from '@mui/material';
import DiceRolls from './DiceRolls';

const DiceRollsPopup = ({ open, onClose, rollsConfig }) => {
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
        <DialogTitle style={{ textAlign: 'center' }}>
          <Typography variant="h4" component="div" style={{ fontWeight: 'bold' }}>
            Dice Rolls
          </Typography>
        </DialogTitle>
        <DialogContent style={{ flex: 1, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <DiceRolls rollsConfig={rollsConfig} />
        </DialogContent>
        <DialogActions style={{ justifyContent: 'center' }}>
          <Button onClick={onClose} color="primary">
            Close
          </Button>
        </DialogActions>
      </Box>
    </Dialog>
  );
};

export default DiceRollsPopup;
