import React from 'react';
import { Card, CardActionArea, CardContent, Typography, Grid, Box } from '@mui/material';
import { useNavigate } from 'react-router';

const ClickableCardsPage = () => {
  const navigate = useNavigate();

  const itemData = [
    { id: 1, title: 'Gun', description: 'GUNS GUNS GUNS.', route: '/quickloot/gun' },
    { id: 2, title: 'Class Mod', description: 'Den Arne heeft er veel werk in gestoken.', route: '/quickloot/classmod' },
    { id: 3, title: 'Shield', description: 'Schild en knuffel.', route: '/quickloot/shield' },
    { id: 4, title: 'Grenade', description: 'Bruno Mars simulator', route: '/quickloot/grenade' },
    { id: 5, title: 'potion', description: '100 Push ups en 2 vuisten', route: '/quickloot/potion' },
  ];

  // TODO
  // const MonsterData = [
  //   { id: 1, title: 'Gun', description: 'This is the description for card 1.', route: '/quickloot/gun' },
  //   { id: 2, title: 'Class Mod', description: 'This is the description for card 2.', route: '/quickloot/classmod' },
  //   { id: 3, title: 'Shield', description: 'This is the description for card 3.', route: '/quickloot/shield' },
  //   { id: 4, title: 'Grenade', description: 'This is the description for card 3.', route: '/quickloot/grenade' },
  //   { id: 5, title: 'potion', description: 'This is the description for card 3.', route: '/quickloot/potion' },
  // ];

  const handleCardClick = (route) => {
    navigate(route);
  };

  return (
    <Box p={2}>
      <Typography variant="h4" gutterBottom >
        Big boy items
      </Typography>
      <Grid container spacing={3} style={{ paddingTop: '20px', paddingBottom: '20px' }}>
        {itemData.map((card) => (
          <Grid item key={card.id} xs={12} sm={6} md={4}>
            <Card>
              <CardActionArea onClick={() => handleCardClick(card.route)}>
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
      <Typography variant="h5" gutterBottom >
        Eigenlijk nog niet zo woop woop, kmoet het nog maken
      </Typography>
    </Box>
  );
};

export default ClickableCardsPage;
