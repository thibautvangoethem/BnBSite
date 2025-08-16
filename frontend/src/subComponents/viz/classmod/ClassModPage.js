import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router';
import { Box, Container, Typography, CircularProgress, Grid, Paper, Button } from '@mui/material';
import EditableField from '../Editablefield';

const Identifiers = ({ id, name, text, isEditing, handleChange }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            Identifiers
        </Typography>
        <EditableField
            label="Name"
            value={name}
            isEditing={isEditing}
            onChange={handleChange}
            name="name"
        />
        <EditableField
            label="Description"
            value={text}
            isEditing={isEditing}
            onChange={handleChange}
            multiline
            name="description"
        />
        <Typography variant="body1" gutterBottom>
            <strong>id:</strong> {id}
        </Typography>
    </Paper>
);

const ClassModDetails = ({ classMod, isEditing, handleChange }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            ClassMod Details
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Class:</strong> {isEditing ? (
                <select
                    name="class_type"
                    value={classMod.class_type || ''}
                    onChange={handleChange}
                >
                    <option value="Commando">Commando</option>
                    <option value="Hunter">Hunter</option>
                    <option value="Gunzerker">Gunzerker</option>
                    <option value="Berseker">Berseker</option>
                    <option value="Psycho">Psycho</option>
                    <option value="Assassin">Assassin</option>
                    <option value="Siren">Siren</option>
                    <option value="Mechromancer">Mechromancer</option>
                </select >
            ) : (classMod.class_type)}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Rarity:</strong> {isEditing ? (
                <select
                    name="rarity"
                    value={classMod.rarity || ''}
                    onChange={handleChange}
                >
                    <option value="Common">Common</option>
                    <option value="Uncommon">Uncommon</option>
                    <option value="Rare">Rare</option>
                    <option value="Epic">Epic</option>
                    <option value="Legendary">Legendary</option>
                    <option value="Unique">Unique</option>
                </select >
            ) : (classMod.rarity)}
        </Typography>
        <EditableField
            label="Prefix"
            value={classMod.prefix}
            isEditing={isEditing}
            onChange={handleChange}
            name="prefix"
        />
        <EditableField
            label="Prefix Effect"
            value={classMod.prefix_effect}
            isEditing={isEditing}
            onChange={handleChange}
            multiline
            name="prefix_effect"
        />
        <EditableField
            label="Suffix"
            value={classMod.suffix}
            isEditing={isEditing}
            onChange={handleChange}
            name="suffix"
        />
        <EditableField
            label="suffix Effect"
            value={classMod.suffix_effect}
            isEditing={isEditing}
            onChange={handleChange}
            multiline
            name="suffix_effect"
        />
    </Paper>
);

const ClassModPage = () => {
    const { id } = useParams();
    const backendUrl = process.env.REACT_APP_BACKEND_URL;
    const [classMod, setClassMod] = useState(null);
    const [loading, setLoading] = useState(true);
    const [isEditing, setIsEditing] = useState(false);

    const handleEditClick = () => {
        setIsEditing(true);
    };

    const handleSaveClick = async () => {
        try {
            const response = await fetch(`${backendUrl}/classmods/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(classMod),
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
                const response = await fetch(`${backendUrl}/classmods/${id}`);
                const result = await response.json();
                setClassMod(result);
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
        setClassMod((prevmod) => ({
            ...prevmod,
            [name]: value,
        }));
    };

    return (
        <Container maxWidth="lg">
            <Box my={4}>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                    <Typography variant="h4" component="div" gutterBottom>
                        Bottom Text
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
                    name={classMod?.name}
                    text={classMod?.description}
                    isEditing={isEditing}
                    handleChange={handleChange}
                />
                <ClassModDetails classMod={classMod}
                    isEditing={isEditing}
                    handleChange={handleChange} />
            </Box>
        </Container >
    );
};

export default ClassModPage;