import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router';
import { Box, Container, Typography, CircularProgress, Grid, Paper, Button } from '@mui/material';

// Component for Identifiers
const Identifiers = ({ id, name, description, isEditing, handleChange }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            Identifiers
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Name:</strong> {isEditing ? (
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
                    value={description || ''}
                    onChange={handleChange}
                    rows="4"
                    style={{ width: '100%' }}
                />
            ) : (
                description || 'None'
            )}
        </Typography>
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
                <Typography variant="body1">
                    <strong>Range:</strong> {isEditing ? (
                        <input
                            type="number"
                            name="range"
                            value={range || ''}
                            onChange={handleChange}
                            onKeyDown={(e) => {
                                if (!/[0-9]/.test(e.key)) {
                                    e.preventDefault();
                                }
                            }}
                        />
                    ) : (
                        range
                    )}
                </Typography>
            </Grid>
            <Grid item xs={12} sm={4}>
                <Typography variant="body1">
                    <strong>Damage Roll:</strong> {isEditing ? (
                        <input
                            type="text"
                            name="dmgroll"
                            value={dmgroll || ''}
                            onChange={handleChange}
                        />
                    ) : (
                        dmgroll
                    )}
                </Typography>
            </Grid>
            <Grid item xs={12} sm={4}>
                <Typography variant="body1">
                    <strong>Low Normal:</strong> {isEditing ? (
                        <input
                            type="number"
                            name="lowNormal"
                            value={lowNormal || ''}
                            onChange={handleChange}
                            onKeyDown={(e) => {
                                if (!/[0-9]/.test(e.key)) {
                                    e.preventDefault();
                                }
                            }}
                        />
                    ) : (
                        lowNormal
                    )}
                </Typography>
            </Grid>
            <Grid item xs={12} sm={4}>
                <Typography variant="body1">
                    <strong>Low Crit:</strong> {isEditing ? (
                        <input
                            type="number"
                            name="lowCrit"
                            value={lowCrit || ''}
                            onChange={handleChange}
                            onKeyDown={(e) => {
                                if (!/[0-9]/.test(e.key)) {
                                    e.preventDefault();
                                }
                            }}
                        />
                    ) : (
                        lowCrit
                    )}
                </Typography>
            </Grid>
            <Grid item xs={12} sm={4}>
                <Typography variant="body1">
                    <strong>Medium Normal:</strong> {isEditing ? (
                        <input
                            type="number"
                            name="mediumNormal"
                            value={mediumNormal || ''}
                            onChange={handleChange}
                            onKeyDown={(e) => {
                                if (!/[0-9]/.test(e.key)) {
                                    e.preventDefault();
                                }
                            }}
                        />
                    ) : (
                        mediumNormal
                    )}
                </Typography>
            </Grid>
            <Grid item xs={12} sm={4}>
                <Typography variant="body1">
                    <strong>Medium Crit:</strong> {isEditing ? (
                        <input
                            type="number"
                            name="mediumCrit"
                            value={mediumCrit || ''}
                            onChange={handleChange}
                            onKeyDown={(e) => {
                                if (!/[0-9]/.test(e.key)) {
                                    e.preventDefault();
                                }
                            }}
                        />
                    ) : (
                        mediumCrit
                    )}
                </Typography>
            </Grid>
            <Grid item xs={12} sm={4}>
                <Typography variant="body1">
                    <strong>High Normal:</strong> {isEditing ? (
                        <input
                            type="number"
                            name="highNormal"
                            value={highNormal || ''}
                            onChange={handleChange}
                            onKeyDown={(e) => {
                                if (!/[0-9]/.test(e.key)) {
                                    e.preventDefault();
                                }
                            }}
                        />
                    ) : (
                        highNormal
                    )}
                </Typography>
            </Grid>
            <Grid item xs={12} sm={4}>
                <Typography variant="body1">
                    <strong>High Crit:</strong> {isEditing ? (
                        <input
                            type="number"
                            name="highCrit"
                            value={highCrit || ''}
                            onChange={handleChange}
                            onKeyDown={(e) => {
                                if (!/[0-9]/.test(e.key)) {
                                    e.preventDefault();
                                }
                            }}
                        />
                    ) : (
                        highCrit
                    )}
                </Typography>
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
            <Typography variant="body1" gutterBottom>
                <strong>Manufacturer Effect:</strong> {isEditing ? (
                    <input
                        type="text"
                        name="manufacturer_effect"
                        value={manufacturerEffect || ''}
                        onChange={handleChange}
                    />
                ) : (
                    manufacturerEffect || 'None'
                )}
            </Typography>
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
                <Typography variant="body1">
                    <strong>Element String:</strong> {isEditing ? (
                        <input
                            type="text"
                            name="elementstr"
                            value={elementstr || ''}
                            onChange={handleChange}
                        />
                    ) : (elementstr || 'None')}
                </Typography>
            </Grid>
        </Grid>
    </Paper>
);

// Component for Prefixes
const Prefixes = ({ prefixes }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            Prefixes
        </Typography>
        {prefixes.map((prefix, index) => (
            <Typography key={index} variant="body1" gutterBottom>
                <strong>Name:</strong> {prefix.name}, <strong>Effect:</strong> {prefix.effect}
            </Typography>
        ))}
    </Paper>
);

// Component for Postfixes
const Postfixes = ({ postfixes }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            Postfixes
        </Typography>
        {postfixes.map((postfix, index) => (
            <Typography key={index} variant="body1" gutterBottom>
                <strong>Name:</strong> {postfix.name}, <strong>Effect:</strong> {postfix.effect}
            </Typography>
        ))}
    </Paper>
);

// Component for Red Texts
const RedTexts = ({ redtexts }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            Red Texts
        </Typography>
        {redtexts.map((redtext, index) => (
            <Typography key={index} variant="body1" gutterBottom color="error">
                <strong>Name:</strong> {redtext.name}, <strong>Effect:</strong> {redtext.effect}
            </Typography>
        ))}
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
                {gun?.prefixes?.length > 0 && <Prefixes prefixes={gun.prefixes} />}
                {gun?.postfixes?.length > 0 && <Postfixes postfixes={gun.postfixes} />}
                {gun?.redtexts?.length > 0 && <RedTexts redtexts={gun.redtexts} />}
            </Box>
        </Container >
    );
};

export default GunPage;
