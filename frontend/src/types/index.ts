export interface Miner {
  id: number;
  model: string;
  manufacturer: string;
  hashrate: number;
  power_consumption: number;
  efficiency: number;
  release_date: string;
  price: number;
}

export interface NetworkTrends {
  difficulty_trend: {
    current: number;
    change_rate: number;
    prediction_next: number;
  };
  hashrate_trend: {
    current: number;
    change_rate: number;
    prediction_next: number;
  };
  correlation: number;
}
