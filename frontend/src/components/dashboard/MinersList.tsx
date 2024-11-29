import { Card, CardContent, Typography, Table, TableBody, TableCell, TableHead, TableRow } from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import { getMiners } from '../../services/api';

export const MinersList = () => {
  const { data } = useQuery(['miners'], getMiners);

  return (
    <Card>
      <CardContent>
        <Typography variant="h5" gutterBottom>Active Miners</Typography>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Hashrate</TableCell>
              <TableCell>Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data?.map((miner) => (
              <TableRow key={miner.id}>
                <TableCell>{miner.name}</TableCell>
                <TableCell>{miner.hashrate}</TableCell>
                <TableCell>{miner.status}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
};
