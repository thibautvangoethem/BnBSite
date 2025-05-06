import React from 'react';
import { Card, CardActionArea, CardContent, Typography, Grid, Box } from '@mui/material';

const ClickableCardsPage = ({ onSerialize }) => {

  const backendUrl = process.env.REACT_APP_BACKEND_URL;

  const itemData = [
    {
      id: 1, title: 'Gun', description: 'GUNS GUNS GUNS.', endpoint: '/guns/rolldescription', post: '/guns/generate'
    },
    { id: 2, title: 'Class Mod', description: 'Den Arne heeft er veel werk in gestoken.', endpoint: '/classmods/rolldescription', post: '/guns/tisnognieaf' },
    { id: 3, title: 'Shield', description: 'Schild en knuffel.', endpoint: '/shields/rolldescription', post: '/shields/generate' },
    { id: 4, title: 'Grenade', description: 'Bruno Mars simulator', endpoint: '/grenades/rolldescription', post: '/guns/tisnognieaf' },
    { id: 5, title: 'potion', description: '100 Push ups en 2 vuisten', endpoint: '/potions/rolldescription', post: '/guns/tisnognieaf' },
  ];

  const MonsterData = [
    {
      id: 1, title: 'Common', description: '1 chiller.', endpoint: '/mobs/common/rolldescription', post: '/guns/tisnognieaf'
    },
    { id: 2, title: 'Elite', description: '1 geezer', endpoint: '/mobs/elite/rolldescription', post: '/guns/tisnognieaf' },
    { id: 3, title: 'miniBoss', description: '1 bijna teamwipe', endpoint: '/mobs/mboss/rolldescription', post: '/guns/tisnognieaf' },
  ];

  const handleCardClick = async (title, endpoint, post) => {
    try {
      const response = await fetch(backendUrl + endpoint);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const rollmodal = await response.json();
      console.log('Data received:', rollmodal);
      rollmodal.label = title + " roll input";
      rollmodal.post = post
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
              <CardActionArea onClick={() => handleCardClick(card.title, card.endpoint, card.post)}>
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
      <Grid container spacing={3} style={{ paddingTop: '20px', paddingBottom: '20px' }}>
        {MonsterData.map((card) => (
          <Grid item key={card.id} xs={12} sm={6} md={4}>
            <Card>
              <CardActionArea onClick={() => handleCardClick(card.title, card.endpoint, card.post)}>
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
    </Box>
  );
};

export default ClickableCardsPage;
