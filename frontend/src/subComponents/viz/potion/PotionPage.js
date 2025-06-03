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
            <strong>text:</strong> {text || 'None'}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>id:</strong> {id}
        </Typography>
    </Paper>
);

const PotionPage = () => {
    const { id } = useParams();
    const backendUrl = process.env.REACT_APP_BACKEND_URL;
    const [potion, setPotion] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(`${backendUrl}/potions/${id}`);
                const result = await response.json();
                setPotion(result);
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
                    Gluck gluck
                </Typography>
                <Identifiers
                    id={id}
                    name={potion?.name}
                    text={potion?.text}
                />
            </Box>
        </Container>
    );
};

export default PotionPage;
