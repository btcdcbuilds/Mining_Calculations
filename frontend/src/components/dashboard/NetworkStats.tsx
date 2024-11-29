import { Card, CardContent, Typography, Grid } from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import { getNetworkStats } from '../../services/api';

export const NetworkStats = () => {
  const { data } = useQuery(['networkStats'], getNetworkStats);

  return (
    <Card>
      <CardContent>
        <Typography variant="h5" gutterBottom>Network Statistics</Typography>
        <Grid container spacing={2}>
          <Grid item xs={4}>
            <Typography>Hashrate: {data?.hashrate}</Typography>
          </Grid>
          <Grid item xs={4}>
            <Typography>Difficulty: {data?.difficulty}</Typography>
          </Grid>
          <Grid item xs={4}>
            <Typography>Block Reward: {data?.block_reward} BTC</Typography>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};
