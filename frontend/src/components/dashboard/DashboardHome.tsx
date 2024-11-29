import { Grid } from '@mui/material';
import { NetworkStats } from './NetworkStats';
import { MinersList } from './MinersList';

export const DashboardHome = () => {
  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <NetworkStats />
      </Grid>
      <Grid item xs={12}>
        <MinersList />
      </Grid>
    </Grid>
  );
};
