from typing import List, Dict
from datetime import datetime
import pandas as pd

class DataValidator:
    @staticmethod
    def validate_historical_data(data: List[Dict]) -> bool:
        required_fields = ['date', 'btc_price', 'network_difficulty', 'hashprice', 'network_hashrate']
        
        for record in data:
            # Check required fields
            if not all(field in record for field in required_fields):
                return False
                
            # Validate data types
            try:
                datetime.strptime(record['date'], '%Y-%m-%d')
                float(record['btc_price'])
                float(record['network_difficulty'])
                float(record['hashprice'])
                float(record['network_hashrate'])
            except (ValueError, TypeError):
                return False
                
            # Validate value ranges
            if float(record['btc_price']) <= 0 or \
               float(record['network_difficulty']) <= 0 or \
               float(record['hashprice']) <= 0 or \
               float(record['network_hashrate']) <= 0:
                return False
                
        return True

    @staticmethod
    def validate_miner_data(data: List[Dict]) -> bool:
        required_fields = ['model', 'manufacturer', 'hashrate', 'power_consumption', 'efficiency', 'release_date']
        
        for record in data:
            # Check required fields
            if not all(field in record for field in required_fields):
                return False
                
            # Validate data types
            try:
                float(record['hashrate'])
                float(record['power_consumption'])
                float(record['efficiency'])
                datetime.strptime(record['release_date'], '%Y-%m-%d')
                if 'price' in record and record['price'] is not None:
                    float(record['price'])
            except (ValueError, TypeError):
                return False
                
            # Validate value ranges
            if float(record['hashrate']) <= 0 or \
               float(record['power_consumption']) <= 0 or \
               float(record['efficiency']) <= 0:
                return False
                
        return True
