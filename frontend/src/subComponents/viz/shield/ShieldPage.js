import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router';
import { Box, Container, Typography, CircularProgress, Grid, Paper, Button } from '@mui/material';
import EditableField from '../Editablefield';

const Identifiers = ({ id, name, description, isEditing, handleChange }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            Identifiers
        </Typography>
        <EditableField
            label="Name"
            value={name}
            isEditing={isEditing}
            onChange={handleChange}
            type="text"
        />
        <EditableField
            label="Description"
            value={description}
            isEditing={isEditing}
            onChange={handleChange}
            multiline={true}
        />
        <Typography variant="body1" gutterBottom>
            <strong>id:</strong> {id}
        </Typography>
    </Paper>
);

// Component for Shield Stats
const ShieldStats = ({ capacity, rechargeRate, rechargeDelay, isEditing, handleChange }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            Shield Stats
        </Typography>
        <Grid container spacing={2}>
            <Grid item xs={12} sm={4}>
                <EditableField
                    label="Capacity"
                    value={capacity}
                    isEditing={isEditing}
                    onChange={handleChange}
                    type="number"
                />
            </Grid>
            <Grid item xs={12} sm={4}>
                <EditableField
                    label="Recharge Rate"
                    value={rechargeRate}
                    isEditing={isEditing}
                    onChange={handleChange}
                    type="number"
                />
            </Grid>
            <Grid item xs={12} sm={4}>
                <EditableField
                    label="Recharge Delay"
                    value={rechargeDelay}
                    isEditing={isEditing}
                    onChange={handleChange}
                    type="number"
                />
            </Grid>
        </Grid>
    </Paper>
);

// Component for Shield Details
const ShieldDetails = ({ manufacturer, rarity, redTextName, isEditing, handleChange }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            Shield Details
        </Typography>
        <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
                <Typography variant="body1">
                    <strong>Manufacturer:</strong> {isEditing ? (
                        <select
                            name="manufacturer"
                            value={manufacturer || ''}
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
                        </select>
                    ) : (manufacturer)}
                </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
                <Typography variant="body1">
                    <strong>Rarity:</strong> {isEditing ? (
                        <select
                            name="rarity"
                            value={rarity || ''}
                            onChange={handleChange}
                        >
                            <option value="Common">Common</option>
                            <option value="Uncommon">Uncommon</option>
                            <option value="Rare">Rare</option>
                            <option value="Epic">Epic</option>
                            <option value="Legendary">Legendary</option>
                            <option value="Unique">Unique</option>
                        </select>
                    ) : (rarity)}
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

const Components = ({ manufacturerEffect, capacitorEffect, batteryEffect, redTextDescription, novaDamage, novaElement, isEditing, handleChange }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            Components
        </Typography>
        <EditableField
            label="Manufacturer Effect"
            value={manufacturerEffect}
            isEditing={isEditing}
            onChange={handleChange}
            multiline={true}
        />
        <EditableField
            label="Capacitor Effect"
            value={capacitorEffect}
            isEditing={isEditing}
            onChange={handleChange}
            multiline={true}
        />
        <EditableField
            label="Battery Effect"
            value={batteryEffect}
            isEditing={isEditing}
            onChange={handleChange}
            multiline={true}
        />
        {novaDamage && (
            <>
                <EditableField
                    label="Nova damage"
                    value={novaDamage}
                    isEditing={isEditing}
                    onChange={handleChange}
                    type="text"
                />
                {novaElement && (
                    <EditableField
                        label="Nova element"
                        value={novaElement}
                        isEditing={isEditing}
                        onChange={handleChange}
                        type="text"
                    />
                )}
            </>
        )}
        {redTextDescription && (
            <Typography variant="body1" color="error" style={{ fontStyle: 'italic' }}>
                {isEditing ? (
                    <textarea
                        name="red_text_description"
                        value={redTextDescription || ''}
                        onChange={handleChange}
                        rows="4"
                        style={{ width: '100%' }}
                    />
                ) : (
                    redTextDescription
                )}
            </Typography>
        )}
    </Paper>
);

const ShieldPage = () => {
    const { id } = useParams();
    const backendUrl = process.env.REACT_APP_BACKEND_URL;
    const [shield, setShield] = useState(null);
    const [loading, setLoading] = useState(true);
    const [isEditing, setIsEditing] = useState(false);

    const handleEditClick = () => {
        setIsEditing(true);
    };

    const handleSaveClick = async () => {
        try {
            const response = await fetch(`${backendUrl}/shields/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(shield),
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

    const handleChange = (e) => {
        const { name, value } = e.target;
        setShield((prevShield) => ({
            ...prevShield,
            [name]: value,
        }));
    };

    return (
        <Container maxWidth="lg">
            <Box my={4}>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                    <Typography variant="h4" component="div" gutterBottom>
                        El Shieldo
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
                    name={shield?.name}
                    description={shield?.description}
                    isEditing={isEditing}
                    handleChange={handleChange}
                />
                <ShieldDetails
                    manufacturer={shield?.manufacturer}
                    rarity={shield?.rarity}
                    redTextName={shield?.red_text_name}
                    isEditing={isEditing}
                    handleChange={handleChange}
                />
                <ShieldStats
                    capacity={shield?.capacity}
                    rechargeRate={shield?.recharge_rate}
                    rechargeDelay={shield?.recharge_delay}
                    isEditing={isEditing}
                    handleChange={handleChange}
                />
                <Components
                    description={shield?.description}
                    manufacturerEffect={shield?.manufacturer_effect}
                    capacitorEffect={shield?.capacitor_effect}
                    batteryEffect={shield?.battery_effect}
                    redTextDescription={shield?.red_text_description}
                    novaDamage={shield?.nova_damage}
                    novaElement={shield?.nova_element}
                    isEditing={isEditing}
                    handleChange={handleChange}
                />
            </Box>
        </Container>
    );
};

export default ShieldPage;