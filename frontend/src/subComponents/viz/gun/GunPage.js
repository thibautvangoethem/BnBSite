import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router';
import { Box, Container, Typography, CircularProgress, Grid, Paper } from '@mui/material';

// Component for Identifiers
const Identifiers = ({ id, name, description }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            Identifiers
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Name:</strong> {name || 'Mr no name'}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Description:</strong> {description || 'None'}
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>ID:</strong> {id}
        </Typography>
    </Paper>
);

// Component for Gun Stats
const GunStats = ({ range, dmgroll, lowNormal, lowCrit, mediumNormal, mediumCrit, highNormal, highCrit }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            Gun Stats
        </Typography>
        <Grid container spacing={2}>
            <Grid item xs={12} sm={4}>
                <Typography variant="body1">
                    <strong>Range:</strong> {range}
                </Typography>
            </Grid>
            <Grid item xs={12} sm={4}>
                <Typography variant="body1">
                    <strong>Damage Roll:</strong> {dmgroll}
                </Typography>
            </Grid>
            <Grid item xs={12} sm={4}>
                <Typography variant="body1">
                    <strong>Low Normal:</strong> {lowNormal}
                </Typography>
            </Grid>
            <Grid item xs={12} sm={4}>
                <Typography variant="body1">
                    <strong>Low Crit:</strong> {lowCrit}
                </Typography>
            </Grid>
            <Grid item xs={12} sm={4}>
                <Typography variant="body1">
                    <strong>Medium Normal:</strong> {mediumNormal}
                </Typography>
            </Grid>
            <Grid item xs={12} sm={4}>
                <Typography variant="body1">
                    <strong>Medium Crit:</strong> {mediumCrit}
                </Typography>
            </Grid>
            <Grid item xs={12} sm={4}>
                <Typography variant="body1">
                    <strong>High Normal:</strong> {highNormal}
                </Typography>
            </Grid>
            <Grid item xs={12} sm={4}>
                <Typography variant="body1">
                    <strong>High Crit:</strong> {highCrit}
                </Typography>
            </Grid>
        </Grid>
    </Paper>
);

// Component for Gun Details
const GunDetails = ({ type, manufacturer, manufacturerEffect, rarity, element, elementstr }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            Gun Details
        </Typography>
        <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
                <Typography variant="body1">
                    <strong>Type:</strong> {type}
                </Typography>
            </Grid>
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
            <Grid item xs={12} sm={6}>
                <Typography variant="body1">
                    <strong>Element:</strong> {element || 'None'}
                </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
                <Typography variant="body1">
                    <strong>Element String:</strong> {elementstr || 'None'}
                </Typography>
            </Grid>
        </Grid>
    </Paper>
);

// Component for Components
const Components = ({ manufacturerEffect, element, elementstr }) => (
    <Paper style={{ padding: '16px', marginBottom: '16px' }}>
        <Typography variant="h5" gutterBottom>
            Components
        </Typography>
        <Typography variant="body1" gutterBottom>
            <strong>Manufacturer Effect:</strong> {manufacturerEffect || 'None'}
        </Typography>
        {element && (
            <Typography variant="body1" gutterBottom>
                <strong>Element:</strong> {element}
            </Typography>
        )}
        {elementstr && (
            <Typography variant="body1" gutterBottom>
                <strong>Element String:</strong> {elementstr}
            </Typography>
        )}
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

    return (
        <Container maxWidth="lg">
            <Box my={4}>
                <Typography variant="h4" component="div" gutterBottom>
                    {gun?.name || 'Gun Details'}
                </Typography>
                <Identifiers
                    id={gun?.id}
                    name={gun?.name}
                    description={gun?.description}
                />
                <GunDetails
                    type={gun?.type}
                    manufacturer={gun?.manufacturer}
                    manufacturerEffect={gun?.manufacturer_effect}
                    rarity={gun?.rarity}
                    element={gun?.element}
                    elementstr={gun?.elementstr}
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
                />
                <Components
                    manufacturerEffect={gun?.manufacturer_effect}
                    element={gun?.element}
                    elementstr={gun?.elementstr}
                />
                <Prefixes prefixes={gun?.prefixes || []} />
                <Postfixes postfixes={gun?.postfixes || []} />
                <RedTexts redtexts={gun?.redtexts || []} />
            </Box>
        </Container>
    );
};

export default GunPage;
