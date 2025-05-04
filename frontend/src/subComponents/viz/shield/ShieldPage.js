import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router';
import { Box, Container, Typography, CircularProgress, Grid, Paper } from '@mui/material';

// Component for Shield Stats
const ShieldStats = ({ capacity, rechargeRate, rechargeDelay }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            Shield Stats
        </Typography>
        <Grid container spacing={2}>
            <Grid item xs={12} sm={4}>
                <Typography variant="body1">
                    <strong>Capacity:</strong> {capacity}
                </Typography>
            </Grid>
            <Grid item xs={12} sm={4}>
                <Typography variant="body1">
                    <strong>Recharge Rate:</strong> {rechargeRate}
                </Typography>
            </Grid>
            <Grid item xs={12} sm={4}>
                <Typography variant="body1">
                    <strong>Recharge Delay:</strong> {rechargeDelay}
                </Typography>
            </Grid>
        </Grid>
    </Paper>
);

// Component for Shield Details
const ShieldDetails = ({ manufacturer, rarity, redText }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            Shield Details
        </Typography>
        <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
                <Typography variant="body1">
                    <strong>Manufacturer:</strong> {manufacturer}
                </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
                <Typography variant="body1">
                    <strong>Rarity:</strong> {rarity}
                </Typography>
            </Grid>
        </Grid>
        {redText && (
            <Typography variant="body1" color="error" style={{ fontStyle: 'italic' }}>
                "{redText}"
            </Typography>
        )}
    </Paper>
);


const identif = ({ description, manufacturerEffect, capacitorEffect, batteryEffect }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            Components Description
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Description:</strong> {description || 'None'}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Manufacturer Effect:</strong> {manufacturerEffect}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Capacitor Effect:</strong> {capacitorEffect}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Battery Effect:</strong> {batteryEffect}
        </Typography>

    </Paper>
);

const Components = ({ description, manufacturerEffect, capacitorEffect, batteryEffect, redText }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            Components Description
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Description:</strong> {description || 'None'}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Manufacturer Effect:</strong> {manufacturerEffect}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Capacitor Effect:</strong> {capacitorEffect}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Battery Effect:</strong> {batteryEffect}
        </Typography>
        {redText && (
            <Typography variant="body1" color="error" style={{ fontStyle: 'italic' }}>
                "{redText}"
            </Typography>
        )}
    </Paper>
);

const ShieldPage = () => {
    const { id } = useParams();
    const backendUrl = process.env.REACT_APP_BACKEND_URL;
    const [shield, setShield] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(`${backendUrl}/shields/${id}`);
                const result = await response.json();
                setShield(result);
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [id, backendUrl]);

    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
                <CircularProgress />
            </Box>
        );
    }

    return (
        <Container maxWidth="lg">
            <Box my={4}>
                <Typography variant="h4" component="div" gutterBottom>
                    El Shieldo
                </Typography>
                <ShieldDetails
                    manufacturer={shield?.manufacturer}
                    rarity={shield?.rarity}
                    redText={shield?.red_text}
                />
                <ShieldStats
                    capacity={shield?.capacity}
                    rechargeRate={shield?.recharge_rate}
                    rechargeDelay={shield?.recharge_delay}
                />
                <Components
                    description={shield?.description}
                    manufacturerEffect={shield?.manufacturer_effect}
                    capacitorEffect={shield?.capacitor_effect}
                    batteryEffect={shield?.battery_effect}
                />
            </Box>
        </Container>
    );
};

export default ShieldPage;
