import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database.database import get_db, Base, engine
from sqlalchemy.orm import Session

client = TestClient(app)

def test_read_miners():
    response = client.get("/api/v1/miners/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_calculate_roi():
    response = client.get("/api/v1/roi/1?electricity_cost=0.12")
    assert response.status_code == 200
    data = response.json()
    assert "roi_days" in data
    assert "daily_profit" in data

def test_compare_miners():
    response = client.get("/api/v1/compare/?miner_ids=1,2")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
