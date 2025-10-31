# Stock AI Technical Analyst

This repository contains a FastAPI backend for stock technical analysis with a React frontend for visualization.

## Features

- **Stock Data Retrieval**: Get historical price data for US and Indian stocks
- **Technical Indicators**: Calculate RSI, MACD, Bollinger Bands, and more
- **Trading Signals**: AI-powered buy/sell/hold recommendations
- **Portfolio Management**: Track your stock positions and performance
- **Timeframe Selection**: Choose from multiple timeframes (1D, 5D, 1M, 3M, 6M, 1Y, 5Y, Max) for data analysis and charting

## Timeframe Feature

The application now supports user-selectable timeframes for viewing stock data and technical indicators. Users can choose from:

- **1D** - 1 day (5-minute intervals)
- **5D** - 5 days (15-minute intervals)
- **1M** - 1 month (hourly intervals)
- **3M** - 3 months (daily intervals)
- **6M** - 6 months (daily intervals)
- **1Y** - 1 year (daily intervals)
- **5Y** - 5 years (daily intervals)
- **Max** - Maximum available data (daily intervals)

The timeframe selector is available in the main dashboard and automatically updates all charts and indicators when changed.

## Setup and Installation

### Backend Setup

1. Create and activate a Python virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start the backend server:
```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## Running Tests

### Backend Tests

Run the Python tests using pytest:
```bash
pytest
```

Run specific test file:
```bash
pytest tests/test_timeframe_mapper.py -v
```

### Frontend Tests

Run the React tests:
```bash
cd frontend
npm test
```

## API Endpoints

### Stock Data

- `GET /api/stocks/{symbol}` - Get historical stock data
  - Query params: `days` (default: 365), `timeframe` (optional: '1d', '5d', '1mo', etc.)
- `GET /api/stocks/{symbol}/latest` - Get latest stock price

### Technical Indicators

- `GET /api/indicators/{symbol}` - Get all technical indicators
  - Query params: `days` (default: 365), `timeframe` (optional)
- `GET /api/indicators/{symbol}/rsi` - Get RSI indicator
- `GET /api/indicators/{symbol}/macd` - Get MACD indicator
- `GET /api/indicators/{symbol}/bollinger-bands` - Get Bollinger Bands

### Trading Signals

- `GET /api/signals/{symbol}` - Get trading signals
  - Query params: `days` (default: 365), `timeframe` (optional)

### Indian Stocks

- `GET /api/indian/stocks/list` - Get list of supported Indian stocks
- `GET /api/indian/stocks/{symbol}` - Get Indian stock data
  - Query params: `days` (default: 365), `timeframe` (optional)
- `GET /api/indian/indicators/{symbol}` - Get indicators for Indian stocks
  - Query params: `days` (default: 365), `timeframe` (optional)

### Portfolio

- `GET /api/portfolio/` - Get portfolio positions
- `POST /api/portfolio/add` - Add position to portfolio
- `DELETE /api/portfolio/{symbol}` - Remove position from portfolio

## Project Structure

```
.
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── utils/
│   └── timeframe_mapper.py # Timeframe to period/interval mapping utility
├── services/
│   ├── stock_service.py    # Stock data fetching service
│   ├── indian_stock_service.py # Indian stock data service
│   ├── indicators_service.py   # Technical indicators calculations
│   ├── signals_service.py      # Trading signals generation
│   └── portfolio_service.py    # Portfolio management
├── tests/
│   └── test_timeframe_mapper.py # Unit tests for timeframe mapper
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── Dashboard.jsx           # Main dashboard
    │   │   ├── TimeframeSelector.jsx   # Timeframe selection component
    │   │   ├── StockChart.jsx          # Stock chart display
    │   │   └── Indicators.jsx          # Technical indicators display
    │   └── services/
    │       └── api.js                  # API client wrapper
    └── package.json
```

## Example Usage

### Using Timeframe Parameter

```bash
# Get 1-month stock data with hourly intervals
curl "http://localhost:8000/api/stocks/AAPL?timeframe=1mo"

# Get 1-day stock data with 5-minute intervals
curl "http://localhost:8000/api/stocks/AAPL?timeframe=1d"

# Get 1-year stock data with daily intervals
curl "http://localhost:8000/api/stocks/AAPL?timeframe=1y"

# Get indicators for a specific timeframe
curl "http://localhost:8000/api/indicators/AAPL?timeframe=3mo"
```

### Legacy Days Parameter (Still Supported)

```bash
# Get last 30 days of data (backward compatible)
curl "http://localhost:8000/api/stocks/AAPL?days=30"
```

## Technologies Used

- **Backend**: Python, FastAPI, yfinance, pandas, numpy
- **Frontend**: React, Axios, Recharts
- **Testing**: pytest (Python), Jest (JavaScript)

## License

This project is open source and available under the MIT License.
