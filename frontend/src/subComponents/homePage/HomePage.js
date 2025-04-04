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
import foto from '../../assets/images/borderlandsfinito.jpg';

const useStyles = makeStyles((theme) => ({
    footer: {
        // backgroundColor: '#333',
        // color: '#fff',
        padding: '10px  ',
        position: 'absolute',
        width: '100%',
        bottom: 0,
    },
    mainContent: {
        marginBottom: '100px', // Ensure content doesn't overlap with footer
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
                            <Typography variant="h2" gutterBottom>
                                Gegroet tot de Bnb website
                            </Typography>
                            <Typography variant="h5">
                                Eindelijk kunnen we dat spel wat sneller doen gaan
                            </Typography>
                            <img
                                src={foto}
                                alt="Description of image"
                                style={{ width: '100%', height: 'auto', marginBottom: '20px' }}
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
