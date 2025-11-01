# Stock AI Technical Analyst

This repository contains a FastAPI backend and React frontend for stock technical analysis with AI-powered insights.

## Features

### Timeframe Selector

The application now includes a **TradingView-style timeframe selector** that allows you to view stock data across different time intervals.

#### Supported Timeframes

- **1m** - 1 minute (7 days of data)
- **3m** - 3 minutes (7 days of data)
- **5m** - 5 minutes (30 days of data)
- **15m** - 15 minutes (60 days of data)
- **30m** - 30 minutes (120 days of data)
- **1h** - 1 hour (2 years of data)
- **4h** - 4 hours (5 years of data)
- **1d** - 1 day (5 years of data) - **Default**
- **1w** - 1 week (maximum available data)
- **1mo** - 1 month (maximum available data)

#### API Usage

##### Get US Stock Data with Timeframe

```bash
# Get daily data (default)
GET /api/stocks/AAPL?days=30

# Get hourly data
GET /api/stocks/AAPL?timeframe=1h

# Get 5-minute data
GET /api/stocks/AAPL?timeframe=5m
```

##### Get Indian Stock Data with Timeframe

```bash
# Get daily data (default)
GET /api/indian/stocks/RELIANCE?days=30

# Get hourly data
GET /api/indian/stocks/RELIANCE?timeframe=1h
```

##### Search Indian Stocks

The API now includes a search endpoint to discover Indian stock symbols easily. The expanded coverage includes approximately **NIFTY 500** stocks loaded from `data/indian_nse_symbols.json`.

```bash
# Search for stocks matching a query
GET /api/indian/stocks/search?query=HDFC

# Returns:
{
  "query": "HDFC",
  "results": ["HDFC", "HDFCBANK", "HDFCLIFE", "HDFCAMC"],
  "total": 4,
  "timestamp": "2024-01-01T12:00:00"
}

# Search by ticker
GET /api/indian/stocks/search?query=TCS.NS

# Returns:
{
  "query": "TCS.NS",
  "results": ["TCS"],
  "total": 1,
  "timestamp": "2024-01-01T12:00:00"
}
```

**Search Features:**
- Case-insensitive search across both symbol keys and NSE tickers
- Partial match support (e.g., "ADANI" returns all Adani group stocks)
- Query validation (1-50 characters required)
- Returns deduplicated, sorted results

##### List All Indian Stocks

```bash
# Get complete list of available Indian stocks
GET /api/indian/stocks/list

# Returns:
{
  "stocks": ["RELIANCE", "TCS", "INFY", ...],
  "total": 180,
  "timestamp": "2024-01-01T12:00:00"
}
```

**Coverage:** The Indian stocks list now includes ~180+ symbols covering NIFTY 50, NIFTY 100, and widely held names up to NIFTY 500, including:
- Banking & Finance: HDFCBANK, ICICIBANK, KOTAKBANK, AXISBANK, SBIN, HDFCLIFE, SBICARD, etc.
- IT: TCS, INFY, WIPRO, HCLTECH, TECHM, LTIM, COFORGE, PERSISTENT, etc.
- Auto & Transportation: MARUTI, TATAMOTORS, EICHERMOT, BAJAJ-AUTO, M&M, etc.
- Pharma: SUNPHARMA, DRREDDY, CIPLA, DIVISLAB, LUPIN, etc.
- Energy & Utilities: RELIANCE, IOC, BPCL, GAIL, NTPC, POWERGRID, etc.
- Consumer: HINDUNILVR, ITC, BRITANNIA, DABUR, MARICO, NESTLEIND, etc.
- Infrastructure: ADANIPORTS, ADANIGREEN, IRCTC, HAL, BEL, etc.

#### Response Format

```json
{
  "symbol": "AAPL",
  "prices": [...],
  "current_price": 150.25,
  "currency": "USD",
  "data_points": 100,
  "timeframe": "1h",
  "last_updated": "2024-01-01T12:00:00"
}
```

#### Provider Limitations

**Important Notes:**
- **1-minute data** is only available for the last 7 days due to Yahoo Finance API limitations
- **Intraday data** (1m, 3m, 5m, 15m, 30m) may not be available for all stocks
- **Market hours**: Intraday data is only collected during market hours
- Historical data availability depends on the stock and the data provider

#### Frontend Usage

The timeframe selector is integrated into the Dashboard component and automatically fetches new data when you select a different timeframe:

1. Enter a stock symbol (e.g., AAPL, TCS, RELIANCE)
2. Click the desired timeframe button (1m, 1h, 1d, etc.)
3. The chart and indicators will automatically update with data for the selected timeframe

## Installation

### Backend

```bash
pip install -r requirements.txt
python main.py
```

### Frontend

```bash
cd frontend
npm install
npm start
```

## Running Tests

```bash
# Run Python tests
pytest tests/

# Run frontend tests
cd frontend
npm test
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

