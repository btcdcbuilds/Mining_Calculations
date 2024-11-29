import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, Typography, Grid } from '@mui/material';
import { api } from '../../services/api';

const NetworkStats = () => {
  const { data: trends } = useQuery(['networkTrends'], api.getNetworkTrends);

  return (
    <Card>
      <CardContent>
        <Typography variant="h6">Network Statistics</Typography>
        <Grid container spacing={2}>
          <Grid item xs={6}>
            <Typography>Hash Rate: {trends?.data.hashrate}</Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography>Difficulty: {trends?.data.difficulty}</Typography>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default NetworkStats;
