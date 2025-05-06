import React, { useState } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Box, Typography, IconButton, TextField, Grid } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

const ShieldModal = (({ open, close, shield }) => {
    console.log(shield);

    return (
        <Dialog open={open} onClose={close} fullWidth
            maxWidth="lg"
            PaperProps={{
                style: {
                    width: '80%',
                    height: '80%',
                },
            }}>
            <Box display="flex" flexDirection="column" height="100%">

                <DialogContent style={{ justifyContent: 'center', alignItems: 'center' }}>
                    <p><strong>Description:</strong> {shield.description || 'None'}</p>
                    <p><strong>Rarity:</strong> {shield.rarity}</p>
                    <p><strong>Manufacturer:</strong> {shield.manufacturer}</p>
                    <p><strong>Capacity:</strong> {shield.capacity}</p>
                    <p><strong>Recharge Rate:</strong> {shield.recharge_rate}</p>
                    <p><strong>Recharge Delay:</strong> {shield.recharge_delay}</p>
                    <p><strong>Manufacturer Effect:</strong> {shield.manufacturer_effect}</p>
                    <p><strong>Capacitor Effect:</strong> {shield.capacitor_effect}</p>
                    <p><strong>Battery Effect:</strong> {shield.battery_effect}</p>
                    {shield.red_text_name && (
                        <>
                            <p><strong>Red Text:</strong></p>
                            <p className="text-red-600 italic">"{shield.red_text_name}"</p>
                            <p className="text-red-600 italic">"{shield.red_text_description}"</p>
                        </>
                    )}
                    {shield.nova_damage && (
                        <>
                            <p><strong>Nova:</strong></p>
                            <p className="text-red-600 italic">"{shield.nova_damage}"</p>
                            <p className="text-red-600 italic">"{shield.nova_element}"</p>
                        </>
                    )}
                </DialogContent>
                <Button
                    onClick={close}
                    className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                >
                    Close
                </Button>
            </Box>
        </Dialog>
    );
});

export default ShieldModal;