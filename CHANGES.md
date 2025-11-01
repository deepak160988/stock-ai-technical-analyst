# CHANGES.md

## Unreleased

### Added
- **NIFTY 500 Universe Refresh Feature**
  - New POST `/api/indian/stocks/refresh` endpoint to refresh Indian stock universe on demand
  - Fetches latest NIFTY 500 constituents from NSE CSV endpoints
  - Supports saving to cache (`config/.nse_nifty500.cache.json`) and optionally to tracked config (`config/nse_nifty500.json`)
  - CLI script `scripts/refresh_nifty500.py` for offline/ops usage
  - Comprehensive error handling with multiple URL fallbacks
  - Returns detailed summary including update status, total stocks, save status, source, timestamp, and errors
  - Universe data now includes symbol, name, and sector information
  - IndianStockService enhanced to load universe from config files with fallback to seed data
  - Tests for refresh functionality and endpoint

## Project Updates

### Date: 2025-10-16
#### Author: deepak160988

### 1. Updates to main.py
- Enhanced functionality for technical analysis of stock data.
- Implemented new algorithms for moving averages and trend analysis.
- Fixed bugs related to data fetching and processing.

### 2. Setup of requirements.txt
- Added essential libraries for data analysis and visualization:
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `requests`
- Ensured compatibility with Python 3.8 and above.

### 3. File Structure Creation
- Organized project files into the following structure:
  - `/src`: Contains source code files.
  - `/data`: For storing datasets.
  - `/tests`: Includes unit tests for the project.
  - `/docs`: Documentation files.

### 4. API Endpoint Additions
- Introduced new API endpoints for:
  - Fetching stock data: `/api/v1/stocks`
  - Analyzing stock trends: `/api/v1/trends`
  - Providing historical data: `/api/v1/historical`

### 5. Configuration Details
- Configuration files placed in `/config` directory.
- Environment variables managed using `dotenv` for sensitive information.
- Database configuration set up for local and production environments.

---

This document serves as a comprehensive record of changes made to the project. For more detailed information on specific updates, please refer to the respective commit history.