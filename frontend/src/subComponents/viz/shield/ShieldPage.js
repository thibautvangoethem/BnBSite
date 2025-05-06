import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router';
import { Box, Container, Typography, CircularProgress, Grid, Paper } from '@mui/material';



const Identifiers = ({ id, name, description }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            Identifiers
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>name:</strong> {name || 'Mr no name'}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Description:</strong> {description || 'None'}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>id:</strong> {id}
        </Typography>
    </Paper>
);
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
const ShieldDetails = ({ manufacturer, rarity, redTextName }) => (
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
        {redTextName && (
            <Typography variant="body1" color="error" style={{ fontStyle: 'italic' }}>
                "{redTextName}"
            </Typography>
        )}
    </Paper>
);

const Components = ({ manufacturerEffect, capacitorEffect, batteryEffect, redTextDescription, novaDamage, novaElement }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            Components
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
        {novaDamage && (
            <>
                <Typography variant="body1" gutterBottom>
                    <strong>Nova damage</strong>"{novaDamage}"
                </Typography>
                {novaElement && (
                    <Typography variant="body1" gutterBottom>
                        <strong>Nova element</strong>"{novaElement}"
                    </Typography>
                )}
            </>
        )}
        {redTextDescription && (
            <Typography variant="body1" color="error" style={{ fontStyle: 'italic' }}>
                "{redTextDescription}"
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
                <Identifiers
                    id={id}
                    name={shield?.name}
                    description={shield?.description}
                />
                <ShieldDetails
                    manufacturer={shield?.manufacturer}
                    rarity={shield?.rarity}
                    redTextName={shield?.red_text_name}
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
                    redTextDescription={shield?.red_text_description}
                    novaDamage={shield?.nova_damage}
                    novaElement={shield?.nove_element}

                />
            </Box>
        </Container>
    );
};

export default ShieldPage;
