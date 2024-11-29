import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, Typography, List, ListItem } from '@mui/material';
import { api } from '../../services/api';

const MinersList = () => {
  const { data: miners } = useQuery(['miners'], api.getMiners);

  return (
    <Card>
      <CardContent>
        <Typography variant="h6">Available Miners</Typography>
        <List>
          {miners?.data.map((miner: any) => (
            <ListItem key={miner.id}>
              <Typography>{miner.name}</Typography>
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default MinersList;
