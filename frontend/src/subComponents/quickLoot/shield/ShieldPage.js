import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Box, Typography, IconButton, TextField, Grid } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

const ShieldPage = () => {
    const { id } = useParams(); // Extract the id parameter from the URL
    const backendUrl = process.env.REACT_APP_BACKEND_URL;
    const [shield, setShield] = useState(null);

    useEffect(() => {
        // Fetch data from the backend
        const fetchData = async () => {
            try {
                const response = await fetch(`${backendUrl}/shields/${id}`);
                const result = await response.json();
                setShield(result);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData();
    }, [id, backendUrl]);

    return (
        <div
            maxWidth="lg"
            PaperProps={{
                style: {
                    width: '80%',
                    height: '80%',
                },
            }}>
            <Box display="flex" flexDirection="column" height="100%">
                <div style={{ justifyContent: 'center', alignItems: 'center' }}>
                    <p><strong>Description:</strong> {shield?.description || 'None'}</p>
                    <p><strong>Rarity:</strong> {shield?.rarity}</p>
                    <p><strong>Manufacturer:</strong> {shield?.manufacturer}</p>
                    <p><strong>Capacity:</strong> {shield?.capacity}</p>
                    <p><strong>Recharge Rate:</strong> {shield?.recharge_rate}</p>
                    <p><strong>Recharge Delay:</strong> {shield?.recharge_delay}</p>
                    <p><strong>Manufacturer Effect:</strong> {shield?.manufacturer_effect}</p>
                    <p><strong>Capacitor Effect:</strong> {shield?.capacitor_effect}</p>
                    <p><strong>Battery Effect:</strong> {shield?.battery_effect}</p>
                    {shield?.red_text && (
                        <p className="text-red-600 italic">"{shield.red_text}"</p>
                    )}
                </div>
            </Box>
        </div>
    );
};

export default ShieldPage;
