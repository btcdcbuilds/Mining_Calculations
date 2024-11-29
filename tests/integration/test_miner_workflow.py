import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database.database import get_db
from datetime import datetime

client = TestClient(app)

def test_complete_miner_workflow():
    # Create new miner
    miner_data = {
        "model": "Test Miner",
        "manufacturer": "Test Corp",
        "hashrate": 100,
        "power_consumption": 3000,
        "efficiency": 30,
        "release_date": datetime.utcnow().isoformat(),
        "price": 10000
    }
    response = client.post("/api/v1/miners/", json=miner_data)
    assert response.status_code == 200
    miner_id = response.json()["id"]

    # Get miner details
    response = client.get(f"/api/v1/miners/{miner_id}")
    assert response.status_code == 200
    assert response.json()["model"] == "Test Miner"

    # Calculate ROI
    response = client.get(f"/api/v1/roi/{miner_id}")
    assert response.status_code == 200
    assert "roi_days" in response.json()

    # Get profitability analysis
    response = client.get(f"/api/v1/profitability/{miner_id}")
    assert response.status_code == 200
    assert "current_metrics" in response.json()
