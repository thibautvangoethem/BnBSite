import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router';
import { Box, Container, Typography, CircularProgress, Grid, Paper, Button } from '@mui/material';



const Identifiers = ({ id, name, text, isEditing, handleChange }) => (
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
            <strong>Description:</strong> {isEditing ? (
                <textarea
                    name="description"
                    value={text || ''}
                    onChange={handleChange}
                    rows="4"
                    style={{ width: '100%' }}
                />
            ) : (
                text || 'None'
            )}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>id:</strong> {id}
        </Typography>
    </Paper>
);

const GrenadeDetails = ({ grenade, isEditing, handleChange }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            Grenade Details
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Rarity:</strong> {isEditing ? (
                <select
                    name="rarity"
                    value={grenade.rarity || ''}
                    onChange={handleChange}
                >
                    <option value="Common">Common</option>
                    <option value="Uncommon">Uncommon</option>
                    <option value="Rare">Rare</option>
                    <option value="Epic">Epic</option>
                    <option value="Legendary">Legendary</option>
                    <option value="Unique">Unique</option>
                </select >
            ) : (grenade.rarity)}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Manufacturer:</strong>{isEditing ? (
                <select
                    name="manufacturer"
                    value={grenade.manufacturer || ''}
                    onChange={handleChange}
                >
                    <option value="Alas">Alas</option>
                    <option value="SkullDugger">SkullDugger</option>
                    <option value="Dahlia">Dahlia</option>
                    <option value="BlackPowder">BlackPowder</option>
                    <option value="MaleFactor">MaleFactor</option>
                    <option value="Hyperius">Hyperius</option>
                    <option value="Feriore">Feriore</option>
                    <option value="Torgue">Torgue</option>
                    <option value="Stoker">Stoker</option>
                </select >
            ) : (grenade.manufacturer)}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Manufacturer Effect:</strong> {isEditing ? (
                <textarea
                    name="description"
                    value={grenade.manufacturer_effect || ''}
                    onChange={handleChange}
                    rows="4"
                    style={{ width: '100%' }}
                />
            ) : (
                grenade.manufacturer_effect || 'None'
            )}
        </Typography>

        <Typography variant="body1" gutterBottom>
            <strong>Damage:</strong> {isEditing ? (
                <input
                    type="text"
                    name="damage"
                    value={grenade.damage || ''}
                    onChange={handleChange}
                />
            ) : (
                grenade.damage
            )}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Radius:</strong> {isEditing ? (
                <input
                    type="text"
                    name="radius"
                    value={grenade.radius || ''}
                    onChange={handleChange}
                />
            ) : (
                grenade.radius
            )}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Primer Effect:</strong> {isEditing ? (
                <textarea
                    name="primer_effect"
                    value={grenade.primer_effect || ''}
                    onChange={handleChange}
                    rows="4"
                    style={{ width: '100%' }}
                />
            ) : (
                grenade.primer_effect
            )}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Detonater Effect:</strong> {isEditing ? (
                <textarea
                    name="detonater_effect"
                    value={grenade.detonater_effect || ''}
                    onChange={handleChange}
                    rows="4"
                    style={{ width: '100%' }}
                />
            ) : (
                grenade.detonater_effect
            )}
        </Typography>

    </Paper>
);

const RedTextDetails = ({ grenade, isEditing, handleChange }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            Red Text Details
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Red Text Name:</strong> {isEditing ? (
                <input
                    type="text"
                    name="red_text_name"
                    value={grenade.red_text_name || ''}
                    onChange={handleChange}
                />
            ) : (
                grenade.red_text_name || 'None'
            )}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Red Text Description:</strong> {isEditing ? (
                <textarea

                    name="red_text_description"
                    value={grenade.red_text_description || ''}
                    onChange={handleChange}
                    rows="4"
                    style={{ width: '100%' }}
                />
            ) : (
                grenade.red_text_description || 'None'
            )}
        </Typography>
    </Paper>
);

const GrenadePage = () => {
    const { id } = useParams();
    const backendUrl = process.env.REACT_APP_BACKEND_URL;
    const [grenade, setGrenade] = useState(null);
    const [loading, setLoading] = useState(true);
    const [isEditing, setIsEditing] = useState(false);
    const handleEditClick = () => {
        setIsEditing(true);
    };

    const handleSaveClick = async () => {
        try {
            const response = await fetch(`${backendUrl}/grenades/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(grenade),
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

    const handleChange = (e) => {
        const { name, value } = e.target;
        setGrenade((prevgren) => ({
            ...prevgren,
            [name]: value,
        }));
    };

    return (
        <Container maxWidth="lg">
            <Box my={4}>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                    <Typography variant="h4" component="div" gutterBottom>
                        Bombaclat
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
                    name={grenade?.name}
                    text={grenade?.description}
                    isEditing={isEditing}
                    handleChange={handleChange}
                />
                <GrenadeDetails grenade={grenade}
                    isEditing={isEditing}
                    handleChange={handleChange} />
                {grenade?.red_text_name || grenade?.red_text_description ? (
                    <RedTextDetails grenade={grenade}
                        isEditing={isEditing}
                        handleChange={handleChange} />
                ) : null}

            </Box>
        </Container >
    );
};

export default GrenadePage;
