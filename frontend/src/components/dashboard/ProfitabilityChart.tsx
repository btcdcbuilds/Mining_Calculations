import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { Paper, Typography } from '@mui/material';
import { api } from '../../services/api';

const ProfitabilityChart = () => {
  const { data, isLoading } = useQuery(['marketAnalysis'], api.getMarketAnalysis);

  if (isLoading) return <div>Loading...</div>;

  return (
    <>
      <Typography variant="h6" gutterBottom>
        Profitability Trends
      </Typography>
      <Paper sx={{ p: 2 }}>
        <LineChart width={800} height={400} data={data?.data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="profitability" stroke="#8884d8" />
          <Line type="monotone" dataKey="hashprice" stroke="#82ca9d" />
        </LineChart>
      </Paper>
    </>
  );
};

export default ProfitabilityChart;
