import React from 'react';
import {
    Container,
    Typography,
    Button,
    IconButton
} from '@mui/material';
import { makeStyles } from '@mui/styles';
import GitHubIcon from '@mui/icons-material/GitHub';
import Mail from '@mui/icons-material/Mail';
import foto from '../../assets/images/borderlands_standard.png';

const useStyles = makeStyles((theme) => ({
    footer: {
        backgroundColor: '##f5f5f5',
        color: '#333',
        padding: '20px',
        boxShadow: '0px 0px 10px rgba(0, 0, 0, 0.1)',
        marginBottom: '100px',
        borderRadius: '10px',
        width: '100%',
    },
    mainContent: {
        marginBottom: '100px',
        backgroundColor: '#f5f5f5',
        padding: '20px',
        borderRadius: '10px',
        boxShadow: '0px 0px 10px rgba(0, 0, 0, 0.1)',
    },
    title: {
        color: '#333',
        fontWeight: 'bold',
        marginBottom: '20px',
        textAlign: 'center',
        fontSize: '2.5rem',
        textShadow: '2px 2px 4px rgba(0, 0, 0, 0.2)',
    },
    subtitle: {
        color: '#666',
        marginBottom: '20px',
    },
    image: {
        width: '100%',
        height: 'auto',
        marginBottom: '20px',
        borderRadius: '10px',
        boxShadow: '0px 0px 10px rgba(0, 0, 0, 0.1)',
    },
}));

const Homepage = () => {
    const emailAddress = 'thibautvangoethem2@gmail.com';
    const classes = useStyles();

    return (
        <>
            <div className={classes.mainContent}>
                <div>
                    <div></div>
                    <div>
                        <Container>
                            <Typography variant="h2" gutterBottom className={classes.title}>
                                Gegroet tot de Bnb website
                            </Typography>
                            <Typography variant="h5" className={classes.subtitle}>
                                Waar is Ruben
                            </Typography>
                            <img
                                src={foto}
                                alt="So apparently eslint asks you to think about usability by filling in this alt field, huh neat"
                                className={classes.image}
                            />
                        </Container>
                    </div>
                </div>
            </div>
            <Container>
                {/* Additional content can go here */}
            </Container>
            <footer className={classes.footer}>
                <Container>
                    <IconButton
                        color="inherit"
                        aria-label="GitHub"
                        component="a"
                        href="https://github.com/thibautvangoethem/BnBSite"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        <GitHubIcon />
                    </IconButton>
                    <IconButton
                        color="inherit"
                        aria-label="Mail"
                        component="a"
                        href={`mailto:${emailAddress}?subject=${encodeURIComponent("super goed feedback over bnb website")}`}
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        <Mail />
                    </IconButton>
                    <Typography variant="body2">
                        Borderlands is owned by Gearbox, no copyright intended.
                    </Typography>
                </Container>
            </footer>
        </>
    );
};

export default Homepage;

