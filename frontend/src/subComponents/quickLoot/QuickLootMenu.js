import React from 'react';
import { Card, CardActionArea, CardContent, Typography, Grid, Box } from '@mui/material';

const ClickableCardsPage = ({ onSerialize }) => {

  const backendUrl = process.env.REACT_APP_BACKEND_URL;

  const itemData = [
    {
      id: 1, title: 'Gun', description: 'GUNS GUNS GUNS.', endpoint: '/guns/rolldescription'
    },
    { id: 2, title: 'Class Mod', description: 'Den Arne heeft er veel werk in gestoken.', endpoint: '/api/quickloot/classmod' },
    { id: 3, title: 'Shield', description: 'Schild en knuffel.', endpoint: '/api/quickloot/shield' },
    { id: 4, title: 'Grenade', description: 'Bruno Mars simulator', endpoint: '/api/quickloot/grenade' },
    { id: 5, title: 'potion', description: '100 Push ups en 2 vuisten', endpoint: '/api/quickloot/potion' },
  ];

  const handleCardClick = async (title, endpoint) => {
    try {
      const response = await fetch(backendUrl + endpoint);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const rollmodal = await response.json();
      console.log('Data received:', rollmodal);
      rollmodal.label = title + " roll input";
      onSerialize(rollmodal);
      // Handle the data as needed
    } catch (error) {
      console.error('Fetch error:', error);
    }
  };

  return (
    <Box p={2}>
      <Typography variant="h4" gutterBottom>
        Big boy items
      </Typography>
      <Grid container spacing={3} style={{ paddingTop: '20px', paddingBottom: '20px' }}>
        {itemData.map((card) => (
          <Grid item key={card.id} xs={12} sm={6} md={4}>
            <Card>
              <CardActionArea onClick={() => handleCardClick(card.title, card.endpoint)}>
                <CardContent>
                  <Typography variant="h5" component="div">
                    {card.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {card.description}
                  </Typography>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>
        ))}
      </Grid>
      <Typography variant="h4" gutterBottom style={{ paddingTop: '40px', paddingBottom: '10px' }}>
        Monster Loot woop woop
      </Typography>
      <Typography variant="h5" gutterBottom>
        Eigenlijk nog niet zo woop woop, moet het nog maken
      </Typography>
    </Box>
  );
};

export default ClickableCardsPage;
