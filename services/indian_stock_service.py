import yfinance as yf
import pandas as pd
import logging
import json
from pathlib import Path
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)


class IndianStockService:
    def __init__(self):
        self.cache = {}
        # Default fallback mapping
        self.indian_stocks = {
            "RELIANCE": "RELIANCE.NS",
            "TCS": "TCS.NS",
            "INFY": "INFY.NS",
            "WIPRO": "WIPRO.NS",
            "HDFCBANK": "HDFCBANK.NS",
            "ICICIBANK": "ICICIBANK.NS",
            "AXISBANK": "AXISBANK.NS",
            "MARUTI": "MARUTI.NS",
            "BHARTI": "BHARTIARTL.NS",
            "SUNPHARMA": "SUNPHARMA.NS",
            "LT": "LT.NS",
            "ASIANPAINT": "ASIANPAINT.NS",
            "ADANIPOWER": "ADANIPOWER.NS",
            "ADANIENT": "ADANIENT.NS",
            "ITC": "ITC.NS",
            "SBIN": "SBIN.NS",
            "INDIGO": "INDIGO.NS",
            "TATAMOTORS": "TATAMOTORS.NS",
            "TATASTEEL": "TATASTEEL.NS",
            "NESTLEIND": "NESTLEIND.NS",
            "POWERGRID": "POWERGRID.NS",
            "NTPC": "NTPC.NS",
            "ONGC": "ONGC.NS",
            "COALINDIA": "COALINDIA.NS",
            "BAJAJFINSV": "BAJAJFINSV.NS",
            "HEROMOTOCO": "HEROMOTOCO.NS",
            "HINDUNILVR": "HINDUNILVR.NS",
            "DMART": "DMART.NS",
            "SHRIRAMFIN": "SHRIRAMFIN.NS",
            "HDFC": "HDFC.NS",
            "CIPLA": "CIPLA.NS",
            "DIVISLAB": "DIVISLAB.NS",
            "LUPIN": "LUPIN.NS",
            "DRREDDY": "DRREDDY.NS",
            "GRASIM": "GRASIM.NS",
            "ULTRACEMCO": "ULTRACEMCO.NS",
            "SBILIFE": "SBILIFE.NS",
            "ICICIGI": "ICICIGI.NS",
            "APOLLOHOSP": "APOLLOHOSP.NS",
            "MAXHEALTH": "MAXHEALTH.NS",
            "MINDTREE": "MINDTREE.NS",
            "PERSISTENT": "PERSISTENT.NS",
        }
        # Load from JSON file if available
        self._load_symbols_from_json()

    def _load_symbols_from_json(self):
        """Load Indian stock symbols from JSON file with fallback to hardcoded mapping"""
        try:
            json_path = Path(__file__).parent.parent / "data" / "indian_nse_symbols.json"
            if json_path.exists():
                with open(json_path, 'r') as f:
                    json_symbols = json.load(f)
                    # Normalize keys to uppercase and ensure values end with .NS
                    for key, value in json_symbols.items():
                        key_upper = key.upper()
                        ticker_value = value
                        if not ticker_value.endswith('.NS') and not ticker_value.endswith('.BO'):
                            ticker_value = f"{ticker_value}.NS"
                        self.indian_stocks[key_upper] = ticker_value
                logger.info(f"✓ Loaded {len(self.indian_stocks)} Indian stock symbols from JSON file")
            else:
                logger.info(f"JSON file not found at {json_path}, using fallback mapping with {len(self.indian_stocks)} symbols")
        except Exception as e:
            logger.warning(f"Failed to load JSON symbols: {e}. Using fallback mapping with {len(self.indian_stocks)} symbols")

    def get_nse_symbol(self, symbol: str) -> str:
        """Convert symbol to NSE format"""
        symbol = symbol.upper()
        if symbol in self.indian_stocks:
            return self.indian_stocks[symbol]
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
            nse_symbol = self.get_nse_symbol(symbol)
            ticker = yf.Ticker(nse_symbol)
            info = ticker.info

            stock_info = {
                "symbol": symbol.upper(),
                "nse_symbol": nse_symbol,
                "name": info.get("longName", info.get("shortName", symbol)),
                "sector": info.get("sector", "Unknown"),
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
            return {
                "symbol": symbol.upper(),
                "name": symbol,
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
        for short_name, nse_symbol in list(self.indian_stocks.items())[:10]:
            try:
                price = self.get_indian_stock_price(short_name)
                stocks.append(
                    {
                        "symbol": short_name,
                        "nse_symbol": nse_symbol,
                        "price_inr": price,
                        "currency": "INR",
                    }
                )
            except Exception as e:
                logger.warning(f"Could not fetch {nse_symbol}: {e}")
        return stocks

    def search_indian_stocks(self, query: str) -> List[str]:
        """Search for Indian stocks by query (searches both symbol keys and ticker values)"""
        try:
            query = query.upper()
            results = set()  # Use set to de-duplicate

            for symbol, nse_symbol in self.indian_stocks.items():
                # Search in symbol key
                if query in symbol:
                    results.add(symbol)
                # Search in NSE ticker value (without .NS/.BO suffix)
                elif query in nse_symbol:
                    results.add(symbol)
                # Also check if query matches the ticker without suffix
                elif query in nse_symbol.replace('.NS', '').replace('.BO', ''):
                    results.add(symbol)

            # Convert to sorted list for consistent results
            results_list = sorted(list(results))
            logger.info(f"Search for '{query}' returned {len(results_list)} results")
            return results_list

        except Exception as e:
            logger.error(f"Error searching Indian stocks: {e}")
            return []


indian_stock_service = IndianStockService()
