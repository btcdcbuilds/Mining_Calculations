import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

export const api = {
  getMiners: () => axios.get(`${API_BASE_URL}/miners/`),
  getNetworkTrends: () => axios.get(`${API_BASE_URL}/network/trends`),
  getROICalculation: (minerId: number, params: any) => 
    axios.get(`${API_BASE_URL}/roi/${minerId}`, { params }),
  getMarketAnalysis: () => axios.get(`${API_BASE_URL}/market/analysis`),
  getProfitability: (minerId: number, params: any) =>
    axios.get(`${API_BASE_URL}/profitability/${minerId}`, { params })
};
