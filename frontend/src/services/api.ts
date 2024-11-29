import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1'
});

export const getNetworkStats = async () => {
  const { data } = await api.get('/network/stats');
  return data;
};

export const getMiners = async () => {
  const { data } = await api.get('/miners');
  return data;
};
