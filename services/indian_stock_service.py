import yfinance as yf
import pandas as pd
import logging
import json
import os
import io
import requests
from datetime import datetime
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)


class IndianStockService:
    def __init__(self):
        self.cache = {}
        # Seed data - will be replaced by loaded data
        self.indian_stocks = {
            "RELIANCE": {"symbol": "RELIANCE", "name": "Reliance Industries Ltd.", "sector": "Oil & Gas"},
            "TCS": {"symbol": "TCS", "name": "Tata Consultancy Services Ltd.", "sector": "IT"},
            "INFY": {"symbol": "INFY", "name": "Infosys Ltd.", "sector": "IT"},
            "WIPRO": {"symbol": "WIPRO", "name": "Wipro Ltd.", "sector": "IT"},
            "HDFCBANK": {"symbol": "HDFCBANK", "name": "HDFC Bank Ltd.", "sector": "Banking"},
            "ICICIBANK": {"symbol": "ICICIBANK", "name": "ICICI Bank Ltd.", "sector": "Banking"},
            "AXISBANK": {"symbol": "AXISBANK", "name": "Axis Bank Ltd.", "sector": "Banking"},
            "MARUTI": {"symbol": "MARUTI", "name": "Maruti Suzuki India Ltd.", "sector": "Automobile"},
            "BHARTIARTL": {"symbol": "BHARTIARTL", "name": "Bharti Airtel Ltd.", "sector": "Telecom"},
            "SUNPHARMA": {"symbol": "SUNPHARMA", "name": "Sun Pharmaceutical Industries Ltd.", "sector": "Pharma"},
        }
        self._load_universe()

    def _load_universe(self):
        """Load NIFTY 500 universe from config files"""
        config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
        cache_file = os.path.join(config_dir, ".nse_nifty500.cache.json")
        config_file = os.path.join(config_dir, "nse_nifty500.json")
        
        # Try cache first, then config file
        for filepath in [cache_file, config_file]:
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list) and len(data) > 0:
                            # Convert list to dict keyed by symbol
                            self.indian_stocks = {
                                item['symbol']: item for item in data
                            }
                            logger.info(f"Loaded {len(self.indian_stocks)} Indian stocks from {filepath}")
                            return
                except Exception as e:
                    logger.warning(f"Failed to load from {filepath}: {e}")
        
        logger.info(f"Using seed data: {len(self.indian_stocks)} Indian stocks")

    def refresh_universe(self, save_to_config: bool = False) -> dict:
        """
        Refresh NIFTY 500 universe from NSE
        
        Args:
            save_to_config: If True, save to config/nse_nifty500.json in addition to cache
            
        Returns:
            Summary dict with update status and metadata
        """
        errors = []
        source = "nse_csv"
        timestamp = datetime.now().astimezone().isoformat()
        
        # URLs to try (in order)
        urls = [
            "https://archives.nseindia.com/content/indices/ind_nifty500list.csv",
            "https://www1.nseindia.com/content/indices/ind_nifty500list.csv",
        ]
        
        # Headers to avoid 403 errors
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.nseindia.com/',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        df = None
        successful_url = None
        
        # Try each URL
        for url in urls:
            try:
                logger.info(f"Attempting to fetch NIFTY 500 from {url}")
                response = requests.get(url, headers=headers, timeout=30)
                response.raise_for_status()
                
                # Parse CSV
                csv_text = response.text
                df = pd.read_csv(io.StringIO(csv_text))
                
                if not df.empty:
                    successful_url = url
                    logger.info(f"Successfully fetched {len(df)} rows from {url}")
                    break
            except Exception as e:
                error_msg = f"Failed to fetch from {url}: {str(e)}"
                logger.warning(error_msg)
                errors.append(error_msg)
                continue
        
        if df is None or df.empty:
            return {
                "updated": False,
                "total": len(self.indian_stocks),
                "saved_cache": False,
                "saved_config": False,
                "source": source,
                "timestamp": timestamp,
                "errors": errors + ["All fetch attempts failed"]
            }
        
        # Normalize data - try different column name variations
        normalized_stocks = []
        
        try:
            # Detect column names (they may vary)
            symbol_col = None
            name_col = None
            sector_col = None
            
            for col in df.columns:
                col_clean = col.strip()
                if col_clean in ['Symbol', 'symbol', 'SYMBOL']:
                    symbol_col = col
                elif col_clean in ['Company Name', 'CompanyName', 'Company', 'NAME', 'Name']:
                    name_col = col
                elif col_clean in ['Industry', 'Sector', 'INDUSTRY', 'Industry Name']:
                    sector_col = col
            
            if not symbol_col:
                errors.append("Could not find Symbol column in CSV")
                return {
                    "updated": False,
                    "total": len(self.indian_stocks),
                    "saved_cache": False,
                    "saved_config": False,
                    "source": source,
                    "timestamp": timestamp,
                    "errors": errors
                }
            
            for _, row in df.iterrows():
                symbol = str(row[symbol_col]).strip().upper()
                # Remove .NS suffix if present
                symbol = symbol.replace('.NS', '')
                
                name = str(row[name_col]).strip() if name_col and pd.notna(row[name_col]) else symbol
                sector = str(row[sector_col]).strip() if sector_col and pd.notna(row[sector_col]) else "Unknown"
                
                normalized_stocks.append({
                    "symbol": symbol,
                    "name": name,
                    "sector": sector
                })
            
            logger.info(f"Normalized {len(normalized_stocks)} stocks")
            
        except Exception as e:
            error_msg = f"Error normalizing data: {str(e)}"
            logger.error(error_msg)
            errors.append(error_msg)
            return {
                "updated": False,
                "total": len(self.indian_stocks),
                "saved_cache": False,
                "saved_config": False,
                "source": source,
                "timestamp": timestamp,
                "errors": errors
            }
        
        # Update in-memory universe
        self.indian_stocks = {
            stock['symbol']: stock for stock in normalized_stocks
        }
        
        # Ensure config directory exists
        config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
        os.makedirs(config_dir, exist_ok=True)
        
        # Save to cache (always)
        cache_file = os.path.join(config_dir, ".nse_nifty500.cache.json")
        saved_cache = False
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(normalized_stocks, f, indent=2, ensure_ascii=False)
            saved_cache = True
            logger.info(f"Saved {len(normalized_stocks)} stocks to cache: {cache_file}")
        except Exception as e:
            error_msg = f"Failed to save cache: {str(e)}"
            logger.error(error_msg)
            errors.append(error_msg)
        
        # Save to config file if requested
        saved_config = False
        if save_to_config:
            config_file = os.path.join(config_dir, "nse_nifty500.json")
            try:
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(normalized_stocks, f, indent=2, ensure_ascii=False)
                saved_config = True
                logger.info(f"Saved {len(normalized_stocks)} stocks to config: {config_file}")
            except Exception as e:
                error_msg = f"Failed to save config: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
        
        return {
            "updated": True,
            "total": len(normalized_stocks),
            "saved_cache": saved_cache,
            "saved_config": saved_config,
            "source": source,
            "timestamp": timestamp,
            "errors": errors
        }

    def get_nse_symbol(self, symbol: str) -> str:
        """Convert symbol to NSE format"""
        symbol = symbol.upper()
        if symbol in self.indian_stocks:
            return f"{symbol}.NS"
        if symbol.endswith(".NS") or symbol.endswith(".BO"):
            return symbol
        return f"{symbol}.NS"

    def validate_indian_symbol(self, symbol: str) -> bool:
        """Validate if Indian stock symbol is valid"""
        try:
            nse_symbol = self.get_nse_symbol(symbol)
            if not nse_symbol:
                return False
            ticker = yf.Ticker(nse_symbol)
            info = ticker.info
            return info.get("symbol") is not None or len(symbol) >= 1
        except Exception as e:
            logger.warning(f"Indian symbol validation failed for {symbol}: {e}")
            return len(symbol) >= 1 and len(symbol) <= 20

    def get_indian_stock_historical_data(
        self,
        symbol: str,
        days: int = 365,
        period: Optional[str] = None,
        interval: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Get historical data for Indian stock

        Args:
            symbol: Indian stock symbol
            days: Number of days (used if period not provided)
            period: yfinance period (e.g., '7d', '1mo', '1y', 'max')
            interval: yfinance interval (e.g., '1m', '1h', '1d')

        Returns:
            DataFrame with historical data
        """
        try:
            nse_symbol = self.get_nse_symbol(symbol)

            # Determine period and interval to use
            if period is None:
                period = f"{days}d"
            if interval is None:
                interval = "1d"

            cache_key = f"{nse_symbol}_{period}_{interval}"
            if cache_key in self.cache:
                logger.info(f"Using cached data for {nse_symbol}")
                return self.cache[cache_key]

            ticker = yf.Ticker(nse_symbol)
            df = ticker.history(period=period, interval=interval)

            if df.empty:
                logger.warning(f"No data found for Indian stock {nse_symbol}")
                return pd.DataFrame()

            self.cache[cache_key] = df
            logger.info(
                f"Retrieved {len(df)} rows of data for {nse_symbol} (period={period}, interval={interval})"
            )
            return df

        except Exception as e:
            logger.error(
                f"Error fetching historical data for Indian stock {symbol}: {e}"
            )
            return pd.DataFrame()

    def get_indian_stock_price(self, symbol: str) -> Optional[float]:
        """Get latest price for Indian stock in INR"""
        try:
            nse_symbol = self.get_nse_symbol(symbol)
            ticker = yf.Ticker(nse_symbol)
            data = ticker.history(period="1d")

            if data.empty:
                logger.warning(f"No price data found for {nse_symbol}")
                return None

            latest_price = data["Close"].iloc[-1]
            logger.info(f"Latest price for {nse_symbol}: ₹{latest_price}")
            return float(latest_price)

        except Exception as e:
            logger.error(f"Error fetching price for Indian stock {symbol}: {e}")
            return None

    def get_indian_stock_info(self, symbol: str) -> Dict:
        """Get information about Indian stock"""
        try:
            symbol_upper = symbol.upper()
            nse_symbol = self.get_nse_symbol(symbol)
            
            # Get basic info from universe if available
            base_info = {}
            if symbol_upper in self.indian_stocks:
                stock_data = self.indian_stocks[symbol_upper]
                base_info = {
                    "name": stock_data.get("name", symbol_upper),
                    "sector": stock_data.get("sector", "Unknown"),
                }
            
            # Try to fetch live data from yfinance
            ticker = yf.Ticker(nse_symbol)
            info = ticker.info

            stock_info = {
                "symbol": symbol_upper,
                "nse_symbol": nse_symbol,
                "name": info.get("longName", info.get("shortName", base_info.get("name", symbol_upper))),
                "sector": info.get("sector", base_info.get("sector", "Unknown")),
                "industry": info.get("industry", "Unknown"),
                "market_cap_inr": info.get("marketCap", 0),
                "pe_ratio": info.get("trailingPE", None),
                "dividend_yield": info.get("dividendYield", None),
                "52_week_high": info.get("fiftyTwoWeekHigh", None),
                "52_week_low": info.get("fiftyTwoWeekLow", None),
                "average_volume": info.get("averageVolume", None),
                "beta": info.get("beta", None),
                "currency": "INR",
                "exchange": "NSE",
            }

            logger.info(f"Retrieved info for Indian stock {nse_symbol}")
            return stock_info

        except Exception as e:
            logger.error(f"Error fetching info for Indian stock {symbol}: {e}")
            symbol_upper = symbol.upper()
            # Fallback to universe data if available
            if symbol_upper in self.indian_stocks:
                stock_data = self.indian_stocks[symbol_upper]
                return {
                    "symbol": symbol_upper,
                    "name": stock_data.get("name", symbol_upper),
                    "sector": stock_data.get("sector", "Unknown"),
                    "currency": "INR",
                    "exchange": "NSE",
                }
            return {
                "symbol": symbol_upper,
                "name": symbol_upper,
                "sector": "Unknown",
                "currency": "INR",
                "exchange": "NSE",
            }

    def get_indian_stock_price_change(
        self, symbol: str, days: int = 1
    ) -> Optional[float]:
        """Get price change percentage for Indian stock"""
        try:
            nse_symbol = self.get_nse_symbol(symbol)
            ticker = yf.Ticker(nse_symbol)
            data = ticker.history(period=f"{days + 1}d")

            if len(data) < 2:
                return None

            old_price = data["Close"].iloc[0]
            new_price = data["Close"].iloc[-1]

            change_percent = ((new_price - old_price) / old_price) * 100
            logger.info(
                f"Price change for {nse_symbol} ({days}d): {change_percent:.2f}%"
            )
            return float(change_percent)

        except Exception as e:
            logger.error(
                f"Error calculating price change for Indian stock {symbol}: {e}"
            )
            return None

    def get_top_indian_stocks(self) -> List[Dict]:
        """Get list of popular Indian stocks"""
        stocks = []
        for symbol, stock_data in list(self.indian_stocks.items())[:10]:
            try:
                price = self.get_indian_stock_price(symbol)
                stocks.append(
                    {
                        "symbol": symbol,
                        "nse_symbol": f"{symbol}.NS",
                        "name": stock_data.get("name", symbol),
                        "sector": stock_data.get("sector", "Unknown"),
                        "price_inr": price,
                        "currency": "INR",
                    }
                )
            except Exception as e:
                logger.warning(f"Could not fetch {symbol}.NS: {e}")
        return stocks

    def search_indian_stocks(self, query: str) -> List[str]:
        """Search for Indian stocks by query"""
        try:
            query = query.upper()
            results = []

            for symbol, stock_data in self.indian_stocks.items():
                name = stock_data.get("name", "").upper()
                sector = stock_data.get("sector", "").upper()
                if query in symbol or query in name or query in sector:
                    results.append(symbol)

            logger.info(f"Search for '{query}' returned {len(results)} results")
            return results

        except Exception as e:
            logger.error(f"Error searching Indian stocks: {e}")
            return []


indian_stock_service = IndianStockService()
