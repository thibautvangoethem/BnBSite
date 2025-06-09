import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router';
import { Box, Container, Typography, CircularProgress, Grid, Paper } from '@mui/material';



const Identifiers = ({ id, name, text }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            Identifiers
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>name:</strong> {name || 'Mr no name'}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>description:</strong> {text || 'None'}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>id:</strong> {id}
        </Typography>
    </Paper>
);

const GrenadeDetails = ({ grenade }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            Grenade Details
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Rarity:</strong> {grenade.rarity}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Manufacturer:</strong> {grenade.manufacturer}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Damage:</strong> {grenade.damage}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Radius:</strong> {grenade.radius}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Manufacturer Effect:</strong> {grenade.manufacturer_effect}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Primer Effect:</strong> {grenade.primer_effect}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Detonater Effect:</strong> {grenade.detonater_effect}
        </Typography>

    </Paper>
);

const RedTextDetails = ({ grenade }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            Red Text Details
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Red Text Name:</strong> {grenade.red_text_name || 'None'}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Red Text Description:</strong> {grenade.red_text_description || 'None'}
        </Typography>
    </Paper>
);

const GrenadePage = () => {
    const { id } = useParams();
    const backendUrl = process.env.REACT_APP_BACKEND_URL;
    const [grenade, setGrenade] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(`${backendUrl}/grenades/${id}`);
                const result = await response.json();
                setGrenade(result);
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
                    Bombaclat
                </Typography>
                <Identifiers
                    id={id}
                    name={grenade?.name}
                    text={grenade?.description}
                />
                <GrenadeDetails grenade={grenade} />
                {grenade?.red_text_name || grenade?.red_text_description ? (
                    <RedTextDetails grenade={grenade} />
                ) : null}

            </Box>
        </Container>
    );
};

export default GrenadePage;
