from datetime import datetime, date
from typing import Dict, List

class MiningCalculator:
    @staticmethod
    def calculate_daily_revenue(
        hashrate: float,  # TH/s
        hashprice: float  # USD/TH/day
    ) -> float:
        """Calculate daily revenue in USD"""
        return hashrate * hashprice

    @staticmethod
    def calculate_daily_power_cost(
        power_consumption: float,  # Watts
        electricity_cost: float,  # USD/kWh
        uptime: float = 1.0  # 0-1
    ) -> float:
        """Calculate daily power cost in USD"""
        daily_kwh = (power_consumption * 24 * uptime) / 1000
        return daily_kwh * electricity_cost

    @staticmethod
    def calculate_daily_profit(
        daily_revenue: float,
        daily_power_cost: float,
        maintenance_cost: float = 0
    ) -> float:
        """Calculate daily profit in USD"""
        return daily_revenue - daily_power_cost - maintenance_cost

    @staticmethod
    def calculate_roi_days(
        initial_investment: float,
        daily_profit: float
    ) -> float:
        """Calculate ROI period in days"""
        if daily_profit <= 0:
            return float('inf')
        return initial_investment / daily_profit

    @staticmethod
    def calculate_efficiency_ratio(
        hashrate: float,  # TH/s
        power_consumption: float  # Watts
    ) -> float:
        """Calculate efficiency in J/TH"""
        return power_consumption / hashrate

    @staticmethod
    def calculate_btc_per_day(
        hashrate: float,  # TH/s
        network_difficulty: float,
        block_reward: float = 6.25
    ) -> float:
        """Calculate expected BTC mined per day"""
        blocks_per_day = 144  # Average number of blocks per day
        network_hashrate = network_difficulty * 2**32 / 600  # H/s
        daily_btc = (hashrate * 10**12 * block_reward * blocks_per_day) / network_hashrate
        return daily_btc
