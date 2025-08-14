import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router';
import { Box, Container, Typography, CircularProgress, Grid, Paper, Button } from '@mui/material';




const Identifiers = ({ id, name, text, isEditing, handleChange }) => {
    const [showText, setShowText] = useState(false);

    const toggleTextVisibility = () => {
        setShowText(!showText);
    };

    return (
        <Paper style={{ padding: '16px', marginBottom: '16px' }}>
            <Typography variant="h5" gutterBottom>
                Identifiers
            </Typography>
            <Typography variant="body1" gutterBottom>
                <strong>name:</strong> {isEditing ? (
                    <input
                        type="text"
                        name="name"
                        value={name || ''}
                        onChange={handleChange}
                    />
                ) : (
                    name || 'Mr no name'
                )}
            </Typography>
            <Typography variant="body1" gutterBottom>
                <strong>text:</strong> {isEditing ? (
                    <textarea
                        name="text"
                        value={text || ''}
                        onChange={handleChange}
                        rows="4"
                        style={{ width: '100%' }}
                    />
                ) : (
                    name?.includes('Tina potion') ? (
                        <>
                            <Button variant="text" onClick={toggleTextVisibility}>
                                {showText ? 'Hide' : 'Show'}
                            </Button>
                            {showText && (text || 'None')}
                        </>
                    ) : (
                        text || 'None'
                    )
                )}
            </Typography>
            <Typography variant="body1" gutterBottom>
                <strong>id:</strong> {id}
            </Typography>
        </Paper>
    );
};



const PotionPage = () => {
    const { id } = useParams();
    const backendUrl = process.env.REACT_APP_BACKEND_URL;
    const [potion, setPotion] = useState(null);
    const [loading, setLoading] = useState(true);
    const [isEditing, setIsEditing] = useState(false);
    const handleEditClick = () => {
        setIsEditing(true);
    };

    const handleSaveClick = async () => {
        try {
            const response = await fetch(`${backendUrl}/potions/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(potion),
            });
            if (response.ok) {
                setIsEditing(false);
            } else {
                console.error('Error saving data');
            }
        } catch (error) {
            console.error('Error saving data:', error);
        }
    };

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

    const handleChange = (e) => {
        const { name, value } = e.target;
        setPotion((prevPotion) => ({
            ...prevPotion,
            [name]: value,
        }));
    };

    return (
        <Container maxWidth="lg">
            <Box my={4}>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                    <Typography variant="h4" component="div" gutterBottom>
                        Gluck gluck
                    </Typography>
                    {isEditing ? (
                        <Button variant="contained" color="primary" onClick={handleSaveClick}>
                            Save
                        </Button>
                    ) : (
                        <Button variant="contained" color="primary" onClick={handleEditClick}>
                            Edit
                        </Button>
                    )}
                </Box>
                <Identifiers
                    id={id}
                    name={potion?.name}
                    text={potion?.text}
                    isEditing={isEditing}
                    handleChange={handleChange}
                />
            </Box>
        </Container>
    );
};

export default PotionPage;
