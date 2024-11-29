import React from 'react';
import { Box, Container, Grid } from '@mui/material';

import NetworkStats from '../NetworkStats/NetworkStats';
import MinersList from '../Miners/MinersList';
import ProfitabilityChart from '../Analytics/ProfitabilityChart';
import ROICalculator from '../Analytics/ROICalculator';

const DashboardLayout = () => {
  return (
    <Container maxWidth="xl">
      <Box sx={{ py: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <ProfitabilityChart />
          </Grid>
          <Grid item xs={12} md={4}>
            <NetworkStats />
          </Grid>
          <Grid item xs={12} md={8}>
            <MinersList />
          </Grid>
          <Grid item xs={12} md={4}>
            <ROICalculator />
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default DashboardLayout;
