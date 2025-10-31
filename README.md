# Stock AI Technical Analyst

This repository contains a FastAPI backend for stock technical analysis with a React frontend that provides real-time stock data, technical indicators, and AI-powered insights.

## Features

- **Multi-Timeframe Analysis**: View stock data across multiple timeframes (1m, 3m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1mo)
- **Technical Indicators**: RSI, MACD, Bollinger Bands, and more
- **US & Indian Stocks**: Support for both US and Indian (NSE) stock markets
- **Portfolio Management**: Track your investments
- **AI-Powered Insights**: Get intelligent stock analysis

## Timeframe Selector

The application now supports TradingView-style timeframe selection for granular data analysis:

### Available Timeframes

- **1m** - 1 minute (7 days of data)
- **3m** - 3 minutes (7 days of data)
- **5m** - 5 minutes (30 days of data)
- **15m** - 15 minutes (60 days of data)
- **30m** - 30 minutes (120 days of data)
- **1h** - 1 hour (2 years of data)
- **4h** - 4 hours (5 years of data)
- **1d** - 1 day (5 years of data) - Default
- **1w** - 1 week (max available data)
- **1mo** - 1 month (max available data)

### API Usage

#### Get Stock Data with Timeframe

```bash
# US Stock with timeframe
GET /api/stocks/AAPL?timeframe=1h

# Indian Stock with timeframe
GET /api/indian/stocks/RELIANCE?timeframe=1d

# Backwards compatible - using days parameter
GET /api/stocks/AAPL?days=30
```

**Query Parameters:**
- `timeframe` (optional): One of the supported timeframes (1m, 3m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1mo)
- `days` (optional): Number of days (used when timeframe is not specified, default: 365)

**Response:**
```json
{
  "symbol": "AAPL",
  "prices": [...],
  "current_price": 150.25,
  "currency": "USD",
  "data_points": 100,
  "timeframe": "1h",
  "last_updated": "2025-10-31T06:30:00"
}
```

## Installation & Running

### Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
# Or using uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### Frontend

```bash
cd frontend
npm install
npm start
```

The frontend will be available at `http://localhost:3000`

## Testing

### Run Backend Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_timeframe.py -v

# Run API integration tests
python -m pytest tests/test_api_timeframe.py -v
```

### Test Coverage

- Unit tests for timeframe mapping logic
- Integration tests for API endpoints
- Validation tests for invalid timeframes

## Provider Notes

This application uses **yfinance** as the data provider. Please note:

- **Intraday data** (1m, 3m, 5m, 15m, 30m) may have limited historical availability
- **Rate limiting** may apply for frequent requests
- Some timeframes may not be available for all stocks
- Data accuracy depends on Yahoo Finance availability

## Development

### Project Structure

```
.
├── backend/
│   ├── routers/         # API route handlers
│   ├── services/        # Business logic services
│   └── models/          # Data models
├── frontend/
│   └── src/
│       ├── components/  # React components
│       └── services/    # API client
├── services/            # Stock, indicators, AI services
├── tests/               # Test files
├── main.py              # FastAPI application entry point
└── requirements.txt     # Python dependencies
```

### Key Files

- `services/stock_service.py` - Stock data fetching with timeframe support
- `frontend/src/components/TimeframeSelector.jsx` - Timeframe UI component
- `frontend/src/components/Dashboard.jsx` - Main dashboard with timeframe integration
- `tests/test_timeframe.py` - Timeframe mapping unit tests
- `tests/test_api_timeframe.py` - API endpoint integration tests

## API Endpoints

- `GET /api/stocks/{symbol}` - Get historical stock data
- `GET /api/indian/stocks/{symbol}` - Get Indian stock data
- `GET /api/indicators/{symbol}` - Get technical indicators
- `GET /api/signals/{symbol}` - Get trading signals
- `GET /api/portfolio/` - Get portfolio data
- `POST /api/portfolio/add` - Add position to portfolio
- `DELETE /api/portfolio/{symbol}` - Remove position from portfolio

## License

This project is for educational and research purposes.
