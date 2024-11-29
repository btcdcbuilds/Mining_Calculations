import React from 'react';
import { ThemeProvider } from '@mui/material';
import { theme } from './theme/theme';
import DashboardLayout from './components/Dashboard/DashboardLayout';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <DashboardLayout />
    </ThemeProvider>
  );
}

export default App;
