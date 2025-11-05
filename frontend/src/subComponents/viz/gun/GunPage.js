import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router';
import { Box, Container, Typography, CircularProgress, Grid, Paper, Button } from '@mui/material';
import EditableField from '../Editablefield';

// Component for Identifiers
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
            <strong>ID:</strong> {id}
        </Typography>
    </Paper>
);

// Component for Gun Stats
const GunStats = ({ range, dmgroll, lowNormal, lowCrit, mediumNormal, mediumCrit, highNormal, highCrit, isEditing, handleChange }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            Gun Stats
        </Typography>
        <Grid container spacing={2}>
            <Grid item xs={12} sm={4}>
                <EditableField
                    label="Range"
                    value={range}
                    isEditing={isEditing}
                    onChange={handleChange}
                    type="number"
                />
            </Grid>
            <Grid item xs={12} sm={4}>
                <EditableField
                    label="Damage Roll"
                    value={dmgroll}
                    isEditing={isEditing}
                    onChange={handleChange}
                    type="text"
                    name="dmgroll"
                />
            </Grid>
            <Grid item xs={12} sm={4}>
                <EditableField
                    label="Low Normal"
                    value={lowNormal}
                    isEditing={isEditing}
                    onChange={handleChange}
                    type="number"
                    name="lowNormal"
                />
            </Grid>
            <Grid item xs={12} sm={4}>
                <EditableField
                    label="Low Crit"
                    value={lowCrit}
                    isEditing={isEditing}
                    onChange={handleChange}
                    type="number"
                    name="lowCrit"
                />
            </Grid>
            <Grid item xs={12} sm={4}>
                <EditableField
                    label="Medium Normal"
                    value={mediumNormal}
                    isEditing={isEditing}
                    onChange={handleChange}
                    type="number"
                    name="mediumNormal"
                />
            </Grid>
            <Grid item xs={12} sm={4}>
                <EditableField
                    label="Medium Crit"
                    value={mediumCrit}
                    isEditing={isEditing}
                    onChange={handleChange}
                    type="number"
                    name="mediumCrit"
                />
            </Grid>
            <Grid item xs={12} sm={4}>
                <EditableField
                    label="High Normal"
                    value={highNormal}
                    isEditing={isEditing}
                    onChange={handleChange}
                    type="number"
                    name="highNormal"
                />
            </Grid>
            <Grid item xs={12} sm={4}>
                <EditableField
                    label="High Crit"
                    value={highCrit}
                    isEditing={isEditing}
                    onChange={handleChange}
                    type="number"
                    name="highCrit"
                />
            </Grid>
        </Grid>
    </Paper>
);

const GunDetails = ({ type, manufacturer, manufacturerEffect, rarity, element, elementstr, isEditing, handleChange }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            Gun Details
        </Typography>
        <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
                <Typography variant="body1">
                    <strong>Type:</strong> {isEditing ? (
                        <select
                            name="type"
                            value={type || ''}
                            onChange={handleChange}
                        >
                            <option value="Assault Rifle">Assault Rifle</option>
                            <option value="Sniper Rifle">Sniper Rifle</option>
                            <option value="Shotgun">Shotgun</option>
                            <option value="Pistol">Pistol</option>
                            <option value="Rocket Launcher">Rocket Launcher</option>
                        </select>
                    ) : (type)}
                </Typography>
            </Grid>
            <EditableField
                label="Manufacturer Effect"
                value={manufacturerEffect}
                isEditing={isEditing}
                onChange={handleChange}
                type="text"
                name="manufacturer_effect"
            />
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
            <Grid item xs={12} sm={6}>
                <Typography variant="body1">
                    <strong>Element:</strong> {isEditing ? (
                        <select
                            name="element"
                            value={element || ''}
                            onChange={handleChange}
                        >
                            <option value="Niets">Niets :(</option>
                            <option value="oepsikwasvergetendatgunsmeerelementskunnenhebbenennuzitdatnietinhetmodel">Multiple</option>
                            <option value="Radiation">Radiation</option>
                            <option value="Corrosive">Corrosive</option>
                            <option value="Shock">Shock</option>
                            <option value="Explosive">Explosive</option>
                            <option value="Incendiary">Incendiary</option>
                            <option value="Cryo">Cryo</option>
                        </select>
                    ) : (element || 'None')}
                </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
                <EditableField
                    label="Element String"
                    value={elementstr}
                    isEditing={isEditing}
                    onChange={handleChange}
                    type="text"
                    name="elementstr"
                />
            </Grid>
        </Grid>
    </Paper>
);

const Prefix = ({ prefix_name, prefix_effect, isEditing, handleChange }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <EditableField
            label="Prefix"
            value={prefix_name}
            isEditing={isEditing}
            onChange={handleChange}
            type="text"
            name="prefix_name"
        />
        <EditableField
            label="Effect"
            value={prefix_effect}
            isEditing={isEditing}
            onChange={handleChange}
            multiline={true}
            name="prefix_effect"
        />
    </Paper>
);


const Redtext = ({ redtext_name, redtext_effect, isEditing, handleChange }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <EditableField
            label="Redtext"
            value={redtext_name}
            isEditing={isEditing}
            onChange={handleChange}
            type="text"
            name="redtext_name"
        />
        <EditableField
            label="Effect"
            value={redtext_effect}
            isEditing={isEditing}
            onChange={handleChange}
            multiline={true}
            name="redtext_effect"
        />
    </Paper>
);

const Parts = ({ barrel_manufacturer, barrel_effect, magazine_manufacturer, magazine_effect, grip_manufacturer, grip_effect, match_bonus, isEditing, handleChange }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <div style={{ display: 'flex', flexDirection: 'row', gap: '16px' }}>
            <div style={{ flex: 1 }}>
                <EditableField
                    label="Barrel"
                    value={barrel_manufacturer}
                    isEditing={isEditing}
                    onChange={handleChange}
                    type="text"
                    name="barrel_manufacturer"
                />
                <EditableField
                    label="Magazine"
                    value={magazine_manufacturer}
                    isEditing={isEditing}
                    onChange={handleChange}
                    type="text"
                    name="magazine_manufacturer"
                />
                <EditableField
                    label="Grip"
                    value={grip_manufacturer}
                    isEditing={isEditing}
                    onChange={handleChange}
                    type="text"
                    name="grip_manufacturer"
                />
            </div>
            <div style={{ flex: 1 }}>
                <EditableField
                    label="Barrel effect"
                    value={barrel_effect}
                    isEditing={isEditing}
                    onChange={handleChange}
                    multiline={true}
                    name="barrel_effect"
                />
                <EditableField
                    label="magazine effect"
                    value={magazine_effect}
                    isEditing={isEditing}
                    onChange={handleChange}
                    multiline={true}
                    name="magazine_effect"
                />
                <EditableField
                    label="Grip effect"
                    value={grip_effect}
                    isEditing={isEditing}
                    onChange={handleChange}
                    multiline={true}
                    name="grip_effect"
                />
            </div>
        </div>
        {match_bonus !== "" && <EditableField
            label="Matching grip:"
            value={match_bonus}
            isEditing={isEditing}
            onChange={handleChange}
            multiline={true}
            name="match_bonus"
        />
        }
    </Paper>
);

const GunPage = () => {
    const { id } = useParams();
    const backendUrl = process.env.REACT_APP_BACKEND_URL;
    const [gun, setGun] = useState(null);
    const [loading, setLoading] = useState(true);
    const [isEditing, setIsEditing] = useState(false);

    const handleEditClick = () => {
        setIsEditing(true);
    };

    const handleSaveClick = async () => {
        try {
            const response = await fetch(`${backendUrl}/guns/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(gun),
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
                const response = await fetch(`${backendUrl}/guns/${id}`);
                const result = await response.json();
                setGun(result);
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
        setGun((prevgun) => ({
            ...prevgun,
            [name]: value,
        }));
    };

    return (
        <Container maxWidth="lg">
            <Box my={4}>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                    <Typography variant="h4" component="div" gutterBottom>
                        {'Gun Details'}
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
                    id={gun?.id}
                    name={gun?.name}
                    description={gun?.description}
                    isEditing={isEditing}
                    handleChange={handleChange}
                />
                <GunDetails
                    type={gun?.type}
                    manufacturer={gun?.manufacturer}
                    manufacturerEffect={gun?.manufacturer_effect}
                    rarity={gun?.rarity}
                    element={gun?.element}
                    elementstr={gun?.elementstr}
                    isEditing={isEditing}
                    handleChange={handleChange}
                />
                <GunStats
                    range={gun?.range}
                    dmgroll={gun?.dmgroll}
                    lowNormal={gun?.lowNormal}
                    lowCrit={gun?.lowCrit}
                    mediumNormal={gun?.mediumNormal}
                    mediumCrit={gun?.mediumCrit}
                    highNormal={gun?.highNormal}
                    highCrit={gun?.highCrit}
                    isEditing={isEditing}
                    handleChange={handleChange}
                />
                {gun?.prefix_name !== "" &&
                    <Prefix
                        prefix_name={gun?.prefix_name}
                        prefix_effect={gun?.prefix_effect}
                        isEditing={isEditing}
                        handleChange={handleChange} />
                }
                {gun?.redtext_name !== "" &&
                    <Redtext
                        redtext_name={gun?.redtext_name}
                        redtext_effect={gun?.redtext_effect}
                        isEditing={isEditing}
                        handleChange={handleChange} />
                }
                <Parts
                    barrel_manufacturer={gun?.barrel_manufacturer}
                    barrel_effect={gun?.barrel_effect}
                    magazine_manufacturer={gun?.magazine_manufacturer}
                    magazine_effect={gun?.magazine_effect}
                    grip_manufacturer={gun?.grip_manufacturer}
                    grip_effect={gun?.grip_effect}
                    match_bonus={gun?.match_bonus}
                    isEditing={isEditing}
                    handleChange={handleChange}
                />
                {/* {gun?.prefixes?.length > 0 && <Prefixes prefixes={gun.prefixes} />}
                {gun?.postfixes?.length > 0 && <Postfixes postfixes={gun.postfixes} />}
                {gun?.redtexts?.length > 0 && <RedTexts redtexts={gun.redtexts} />} */}
            </Box>
        </Container>
    );
};

export default GunPage;