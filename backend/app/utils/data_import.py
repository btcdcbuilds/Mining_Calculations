import pandas as pd
from typing import List, Dict
from datetime import datetime
from sqlalchemy.orm import Session
from ..models.historical_data import HistoricalData
from ..models.miner import MinerModel

class DataImporter:
    @staticmethod
    def import_historical_data(db: Session, data: List[Dict]) -> List[HistoricalData]:
        historical_records = []
        for record in data:
            db_record = HistoricalData(
                date=datetime.strptime(record['date'], '%Y-%m-%d').date(),
                btc_price=float(record['btc_price']),
                network_difficulty=float(record['network_difficulty']),
                hashprice=float(record['hashprice']),
                network_hashrate=float(record['network_hashrate'])
            )
            historical_records.append(db_record)
            db.add(db_record)
        db.commit()
        return historical_records

    @staticmethod
    def import_miners(db: Session, data: List[Dict]) -> List[MinerModel]:
        miner_records = []
        for record in data:
            db_miner = MinerModel(
                model=record['model'],
                manufacturer=record['manufacturer'],
                hashrate=float(record['hashrate']),
                power_consumption=float(record['power_consumption']),
                efficiency=float(record['efficiency']),
                release_date=datetime.strptime(record['release_date'], '%Y-%m-%d'),
                price=float(record['price']) if record.get('price') else None
            )
            miner_records.append(db_miner)
            db.add(db_miner)
        db.commit()
        return miner_records

    @staticmethod
    def import_csv(filepath: str, date_columns: List[str] = None) -> List[Dict]:
        df = pd.read_csv(filepath)
        if date_columns:
            for col in date_columns:
                df[col] = pd.to_datetime(df[col])
        return df.to_dict('records')
