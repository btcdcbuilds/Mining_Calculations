import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import NetworkStats from '../NetworkStats';

describe('NetworkStats Component', () => {
  test('renders network statistics', () => {
    const mockData = {
      difficulty: 55.85e12,
      hashrate: 500.23,
      blockReward: 6.25
    };
    
    render(<NetworkStats {...mockData} />);
    
    expect(screen.getByText(/Network Difficulty/i)).toBeInTheDocument();
    expect(screen.getByText(/Network Hashrate/i)).toBeInTheDocument();
    expect(screen.getByText(/Block Reward/i)).toBeInTheDocument();
  });

  test('formats values correctly', () => {
    const mockData = {
      difficulty: 55.85e12,
      hashrate: 500.23,
      blockReward: 6.25
    };
    
    render(<NetworkStats {...mockData} />);
    
    expect(screen.getByText(/55.85T/)).toBeInTheDocument();
    expect(screen.getByText(/500.23 EH\/s/)).toBeInTheDocument();
    expect(screen.getByText(/6.25 BTC/)).toBeInTheDocument();
  });
});
