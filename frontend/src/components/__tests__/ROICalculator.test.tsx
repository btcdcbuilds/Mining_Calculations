import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import ROICalculator from '../ROICalculator';

describe('ROICalculator Component', () => {
  test('calculates ROI correctly', () => {
    render(<ROICalculator />);
    
    fireEvent.change(screen.getByLabelText(/Initial Investment/i), {
      target: { value: '10000' }
    });
    fireEvent.change(screen.getByLabelText(/Daily Revenue/i), {
      target: { value: '50' }
    });
    fireEvent.change(screen.getByLabelText(/Daily Cost/i), {
      target: { value: '10' }
    });
    
    fireEvent.click(screen.getByText(/Calculate ROI/i));
    
    expect(screen.getByText(/250 days/i)).toBeInTheDocument();
  });

  test('validates input fields', () => {
    render(<ROICalculator />);
    
    fireEvent.click(screen.getByText(/Calculate ROI/i));
    
    expect(screen.getByText(/Please fill all fields/i)).toBeInTheDocument();
  });
});
