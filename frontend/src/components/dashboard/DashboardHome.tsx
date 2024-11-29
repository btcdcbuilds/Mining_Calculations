import React from 'react';
import { Grid } from '@mui/material';
import MinersList from './MinersList';
import NetworkStats from './NetworkStats';

const DashboardHome = () => {
  return (
    <Grid container spacing={3}>
      <Grid item xs={12} md={8}>
        <NetworkStats />
      </Grid>
      <Grid item xs={12} md={4}>
        <MinersList />
      </Grid>
    </Grid>
  );
};

export default DashboardHome;
