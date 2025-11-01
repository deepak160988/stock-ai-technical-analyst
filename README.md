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

## Indian Stocks

The API provides comprehensive coverage of Indian stocks listed on the NSE (National Stock Exchange), with support for approximately **NIFTY 500** companies.

### Coverage

Indian stock symbols are loaded from `data/indian_nse_symbols.json`, which contains a broad mapping of Indian stock symbols to their Yahoo Finance NSE tickers (ending with `.NS`). The coverage includes:

- **NIFTY 50**: All major blue-chip companies
- **NIFTY 100**: Top 100 companies by market capitalization
- **NIFTY 500**: Broader market coverage including mid-cap and small-cap companies
- Widely held and actively traded stocks

The mapping is designed to be easily extensible. To add more symbols, simply update the `data/indian_nse_symbols.json` file.

### API Endpoints

#### 1. List Indian Stocks

Get a list of all available Indian stock symbols.

**Default Behavior (backward compatible):**
```bash
GET /api/indian/stocks/list
```

**Response:**
```json
{
  "stocks": ["RELIANCE", "TCS", "HDFCBANK", "INFY", ...],
  "total": 300,
  "timestamp": "2024-01-01T12:00:00"
}
```

**With Tickers:**
```bash
GET /api/indian/stocks/list?include_tickers=true
# or
GET /api/indian/stocks/list?include_tickers=1
```

**Response:**
```json
{
  "stocks": [
    {"symbol": "RELIANCE", "ticker": "RELIANCE.NS"},
    {"symbol": "TCS", "ticker": "TCS.NS"},
    {"symbol": "HDFCBANK", "ticker": "HDFCBANK.NS"},
    ...
  ],
  "total": 300,
  "timestamp": "2024-01-01T12:00:00"
}
```

**Parameters:**
- `include_tickers` (optional, boolean, default: `false`): 
  - When `false` or `0`: Returns a list of symbol strings (default behavior)
  - When `true` or `1`: Returns a list of objects with `symbol` and `ticker` properties

#### 2. Search Indian Stocks

Search for Indian stocks by symbol or ticker. The search is case-insensitive and matches partial strings in both symbol keys and NSE tickers.

```bash
GET /api/indian/stocks/search?query=HDFC
```

**Response:**
```json
{
  "query": "HDFC",
  "results": ["HDFC", "HDFCBANK", "HDFCLIFE", "HDFCAMC"],
  "total": 4,
  "timestamp": "2024-01-01T12:00:00"
}
```

**More Examples:**

Search by ticker:
```bash
GET /api/indian/stocks/search?query=TCS.NS
# Returns: ["TCS"]
```

Search for ADANI group companies:
```bash
GET /api/indian/stocks/search?query=ADANI
# Returns: ["ADANIENT", "ADANIPORTS", "ADANIGREEN", "ADANIPOWER", "ADANITRANS"]
```

Search is case-insensitive:
```bash
GET /api/indian/stocks/search?query=reliance
# Returns: ["RELIANCE"]
```

**Parameters:**
- `query` (required, string, 1-50 characters): Search query
  - Searches both symbol keys and ticker values
  - Case-insensitive
  - Returns deduplicated results
  - Blank or whitespace-only queries return `400 Bad Request`

**Response Fields:**
- `query`: The search query as provided
- `results`: Array of matching symbol keys (deduplicated and sorted)
- `total`: Number of results
- `timestamp`: ISO 8601 timestamp of the response

#### 3. Get Indian Stock Data

Get historical data for an Indian stock:

```bash
GET /api/indian/stocks/RELIANCE?days=30
GET /api/indian/stocks/TCS?timeframe=1h
```

#### 4. Get Indian Stock Latest Price

Get the latest price for an Indian stock:

```bash
GET /api/indian/stocks/RELIANCE/latest
```

### Implementation Details

- **JSON Loading**: On initialization, the service attempts to load `data/indian_nse_symbols.json`. If the file is present, it merges with the in-code mapping (JSON takes precedence). If the file is missing or invalid, the service logs a warning and falls back to the in-code mapping.
- **Normalization**: All symbol keys are normalized to UPPERCASE. Ticker values must end with `.NS` (NSE) or `.BO` (BSE).
- **Search**: The `search_indian_stocks()` method searches both keys and tickers case-insensitively and returns deduplicated symbol keys.
- **Backward Compatibility**: Existing endpoints remain unchanged by default. The list endpoint only returns additional data when explicitly requested via the `include_tickers` parameter.

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

