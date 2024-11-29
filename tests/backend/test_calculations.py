import pytest
from backend.app.utils.calculations import MiningCalculator

def test_calculate_daily_revenue():
    calculator = MiningCalculator()
    hashrate = 100  # TH/s
    hashprice = 0.1  # USD/TH/day
    expected = 10.0  # USD/day
    assert calculator.calculate_daily_revenue(hashrate, hashprice) == expected

def test_calculate_daily_power_cost():
    calculator = MiningCalculator()
    power = 3000  # Watts
    electricity_cost = 0.12  # USD/kWh
    expected = 8.64  # USD/day
    assert calculator.calculate_daily_power_cost(power, electricity_cost) == expected

def test_calculate_roi_days():
    calculator = MiningCalculator()
    investment = 10000  # USD
    daily_profit = 20  # USD/day
    expected = 500  # days
    assert calculator.calculate_roi_days(investment, daily_profit) == expected

def test_calculate_efficiency_ratio():
    calculator = MiningCalculator()
    hashrate = 100  # TH/s
    power = 3000  # Watts
    expected = 30  # J/TH
    assert calculator.calculate_efficiency_ratio(hashrate, power) == expected
