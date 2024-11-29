from datetime import datetime, date, timedelta
from typing import Dict, List, Optional

class MiningCalculator:
    @staticmethod
    def calculate_daily_revenue(hashrate: float, hashprice: float) -> float:
        return hashrate * hashprice

    @staticmethod
    def calculate_daily_power_cost(power_consumption: float, electricity_cost: float, uptime: float = 1.0) -> float:
        daily_kwh = (power_consumption * 24 * uptime) / 1000
        return daily_kwh * electricity_cost

    @staticmethod
    def calculate_daily_profit(daily_revenue: float, daily_power_cost: float, maintenance_cost: float = 0) -> float:
        return daily_revenue - daily_power_cost - maintenance_cost

    @staticmethod
    def calculate_roi_days(initial_investment: float, daily_profit: float) -> float:
        return float('inf') if daily_profit <= 0 else initial_investment / daily_profit

    @staticmethod
    def calculate_efficiency_ratio(hashrate: float, power_consumption: float) -> float:
        return power_consumption / hashrate

    @staticmethod
    def calculate_btc_per_day(hashrate: float, network_difficulty: float, block_reward: float = 6.25) -> float:
        blocks_per_day = 144
        network_hashrate = network_difficulty * 2**32 / 600
        return (hashrate * 10**12 * block_reward * blocks_per_day) / network_hashrate

    def calculate_all_metrics(self, hashrate: float, power_consumption: float, 
                            electricity_cost: float, uptime: float = 1.0, 
                            maintenance_cost: float = 0, initial_investment: float = 0) -> Dict:
        daily_revenue = self.calculate_daily_revenue(hashrate, electricity_cost)
        daily_power_cost = self.calculate_daily_power_cost(power_consumption, electricity_cost, uptime)
        daily_profit = self.calculate_daily_profit(daily_revenue, daily_power_cost, maintenance_cost)
        roi_days = self.calculate_roi_days(initial_investment, daily_profit)
        efficiency = self.calculate_efficiency_ratio(hashrate, power_consumption)

        return {
            "daily_profit": daily_profit,
            "roi_days": roi_days,
            "efficiency": efficiency,
            "power_cost": daily_power_cost,
            "revenue": daily_revenue,
            "break_even_date": datetime.now() + timedelta(days=roi_days),
            "profit_ratio": daily_profit / initial_investment if initial_investment > 0 else 0
        }

    def calculate_historical_metrics(self, hashrate: float, power_consumption: float,
                                  electricity_cost: float, btc_price: float,
                                  network_difficulty: float, hashprice: float) -> Dict:
        daily_revenue = self.calculate_daily_revenue(hashrate, hashprice)
        daily_power_cost = self.calculate_daily_power_cost(power_consumption, electricity_cost)
        daily_profit = self.calculate_daily_profit(daily_revenue, daily_power_cost)
        btc_mined = self.calculate_btc_per_day(hashrate, network_difficulty)

        return {
            "revenue": daily_revenue,
            "power_cost": daily_power_cost,
            "profit": daily_profit,
            "btc_mined": btc_mined,
            "btc_value": btc_mined * btc_price
        }

    @staticmethod
    def calculate_profit_trend(historical_metrics: List[Dict]) -> Dict:
        if not historical_metrics:
            return None

        profits = [h["profit"] for h in historical_metrics]
        return {
            "min": min(profits),
            "max": max(profits),
            "average": sum(profits) / len(profits),
            "trend": "up" if profits[-1] > profits[0] else "down"
        }
