# Bitcoin Mining Analytics Tool

## Project Overview
A comprehensive FastAPI-based analytics tool for Bitcoin mining operations, providing detailed calculations, historical analysis, and profitability metrics.

## Current Implementation Status

### ✅ Completed Features

#### Backend Infrastructure
- FastAPI application setup with SQLite database
- SQLAlchemy models for miners and historical data
- Alembic migrations configuration
- CORS middleware enabled
- Base API structure with error handling

#### API Endpoints Implemented
1. **Miner Management** (`/api/v1/miners/`)
   - List all miners
   - Create new miner
   - Get miner by ID

2. **Historical Data** (`/api/v1/historical/`)
   - Get historical data with date range filtering
   - Get latest metrics
   - Get statistical summaries

3. **ROI Analysis** (`/api/v1/roi/{miner_id}`)
   - Calculate ROI metrics
   - Break-even analysis
   - Profit projections

4. **Miner Comparison** (`/api/v1/compare/`)
   - Compare multiple miners
   - Efficiency analysis
   - Profitability comparison

5. **Advanced Analytics**
   - Network trends (`/api/v1/network/trends`)
   - Depreciation analysis (`/api/v1/depreciation/{miner_id}`)
   - Portfolio management (`/api/v1/portfolio/summary`)
   - Cost basis tracking (`/api/v1/cost-basis/{miner_id}`)
   - Market analysis (`/api/v1/market/analysis`)

#### Frontend Development
- React dashboard setup
- Material-UI theme implementation
- API integration services
- Core components:
  - Dashboard layout
  - Network statistics
  - Miner management interface
  - ROI calculator
  - Profitability charts
  - Market analysis views

#### Data Management
- Data import scripts
- Data validation
- Export functionality
- Automated updates

### 📋 Remaining Tasks

1. **Advanced Features**
   - [ ] Machine learning price predictions
   - [ ] Advanced portfolio optimization
   - [ ] Energy efficiency analysis
   - [ ] Risk assessment system
   - [ ] Alert system for profitability thresholds

2. **Documentation**
   - [ ] API documentation with Swagger UI
   - [ ] Installation guide
   - [ ] User manual
   - [ ] Development guide

3. **Deployment**
   - [ ] Docker configuration
   - [ ] CI/CD pipeline
   - [ ] Production deployment guide
   - [ ] Monitoring setup

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- SQLite

### Installation
1. Clone the repository
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   cd frontend && npm install
   ```
4. Initialize database:
   ```bash
   alembic upgrade head
   ```
5. Run the application:
   ```bash
   # Backend
   uvicorn backend.app.main:app --reload
   # Frontend
   cd frontend && npm start
   ```

### API Documentation
Once running, access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Contributing
1. Create a new branch for features
2. Make changes and test
3. Submit pull request with detailed description