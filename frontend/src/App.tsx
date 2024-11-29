import React from 'react';
import { ThemeProvider } from '@mui/material';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { theme } from './theme/theme';
import DashboardLayout from './components/Dashboard/DashboardLayout';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <DashboardLayout />
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;
