import yfinance as yf
import pandas as pd
import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

# Allowed timeframe values
ALLOWED_TIMEFRAMES = ['1m', '3m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1mo']

# Canonical mapping of timeframes to yfinance period and interval
TIMEFRAME_MAPPING = {
    '1m': {'period': '7d', 'interval': '1m'},
    '3m': {'period': '7d', 'interval': '3m'},
    '5m': {'period': '30d', 'interval': '5m'},
    '15m': {'period': '60d', 'interval': '15m'},
    '30m': {'period': '120d', 'interval': '30m'},
    '1h': {'period': '2y', 'interval': '60m'},
    '4h': {'period': '5y', 'interval': '4h'},
    '1d': {'period': '5y', 'interval': '1d'},
    '1w': {'period': 'max', 'interval': '1wk'},
    '1mo': {'period': 'max', 'interval': '1mo'}
}

def map_timeframe(timeframe: Optional[str] = None) -> Dict[str, str]:
    """
    Map timeframe to yfinance period and interval parameters.
    
    Args:
        timeframe: One of the allowed timeframe values (1m, 3m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1mo)
                  If None or not provided, defaults to None (will use days parameter instead)
    
    Returns:
        Dictionary with 'period' and 'interval' keys, or empty dict if timeframe is None
    
    Raises:
        ValueError: If timeframe is not in the allowed list
    """
    if timeframe is None:
        return {}
    
    if timeframe not in ALLOWED_TIMEFRAMES:
        raise ValueError(f"Invalid timeframe '{timeframe}'. Must be one of: {ALLOWED_TIMEFRAMES}")
    
    return TIMEFRAME_MAPPING[timeframe]

class StockService:
    def __init__(self):
        self.cache = {}
        self.valid_symbols = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN', 'META', 'NVDA', 'JPM', 'V', 'JNJ', 'WMT', 'PG', 'KO', 'DIS', 'NFLX', 'AMD', 'INTC', 'CSCO', 'ADBE', 'CRM']
    
    def validate_symbol(self, symbol: str) -> bool:
        """Validate if stock symbol is valid"""
        try:
            if not symbol or len(symbol) < 1:
                return False
            # Try to fetch basic info to validate symbol
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return info.get('symbol') is not None or len(symbol) <= 5
        except Exception as e:
            logger.warning(f"Symbol validation failed for {symbol}: {e}")
            return len(symbol) >= 1 and len(symbol) <= 5
    
    def get_historical_data(self, symbol: str, days: int = 365, timeframe: Optional[str] = None) -> pd.DataFrame:
        """
        Get historical stock data
        
        Args:
            symbol: Stock ticker symbol
            days: Number of days of historical data (used when timeframe is None)
            timeframe: Optional timeframe (1m, 3m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1mo)
        
        Returns:
            DataFrame with historical stock data
        """
        try:
            if not symbol:
                return pd.DataFrame()
            
            # Determine whether to use timeframe or days
            if timeframe:
                tf_params = map_timeframe(timeframe)
                cache_key = f"{symbol}_{timeframe}"
                period = tf_params['period']
                interval = tf_params['interval']
            else:
                cache_key = f"{symbol}_{days}d"
                period = f"{days}d"
                interval = '1d'
            
            # Check cache first
            if cache_key in self.cache:
                logger.info(f"Using cached data for {symbol} (cache_key: {cache_key})")
                return self.cache[cache_key]
            
            # Fetch data from yfinance
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)
            
            if df.empty:
                logger.warning(f"No data found for symbol {symbol}")
                return pd.DataFrame()
            
            # Cache the data
            self.cache[cache_key] = df
            logger.info(f"Retrieved {len(df)} rows of data for {symbol} with period={period}, interval={interval}")
            return df
        
        except ValueError as e:
            logger.error(f"Invalid timeframe parameter: {e}")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error fetching historical data for {symbol}: {e}")
            return pd.DataFrame()
    
    def get_latest_price(self, symbol: str) -> Optional[float]:
        """Get latest stock price"""
        try:
            if not symbol:
                return None
            
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            
            if data.empty:
                logger.warning(f"No price data found for {symbol}")
                return None
            
            latest_price = data['Close'].iloc[-1]
            logger.info(f"Latest price for {symbol}: ${latest_price}")
            return float(latest_price)
        
        except Exception as e:
            logger.error(f"Error fetching latest price for {symbol}: {e}")
            return None
    
    def get_stock_info(self, symbol: str) -> Dict:
        """Get stock information"""
        try:
            if not symbol:
                return {}
            
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            stock_info = {
                "symbol": symbol,
                "name": info.get("longName", info.get("shortName", symbol)),
                "sector": info.get("sector", "Unknown"),
                "industry": info.get("industry", "Unknown"),
                "market_cap": info.get("marketCap", 0),
                "pe_ratio": info.get("trailingPE", None),
                "dividend_yield": info.get("dividendYield", None),
                "52_week_high": info.get("fiftyTwoWeekHigh", None),
                "52_week_low": info.get("fiftyTwoWeekLow", None),
                "average_volume": info.get("averageVolume", None),
                "beta": info.get("beta", None),
            }
            
            logger.info(f"Retrieved info for {symbol}")
            return stock_info
        
        except Exception as e:
            logger.error(f"Error fetching stock info for {symbol}: {e}")
            return {
                "symbol": symbol,
                "name": symbol,
                "sector": "Unknown",
                "industry": "Unknown",
            }
    
    def get_price_change(self, symbol: str, days: int = 1) -> Optional[float]:
        """Get price change percentage"""
        try:
            if not symbol:
                return None
            
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=f"{days + 1}d")
            
            if len(data) < 2:
                return None
            
            old_price = data['Close'].iloc[0]
            new_price = data['Close'].iloc[-1]
            
            change_percent = ((new_price - old_price) / old_price) * 100
            logger.info(f"Price change for {symbol} ({days}d): {change_percent:.2f}%")
            return float(change_percent)
        
        except Exception as e:
            logger.error(f"Error calculating price change for {symbol}: {e}")
            return None
    
    def get_moving_average(self, symbol: str, window: int = 20) -> Optional[float]:
        """Get moving average"""
        try:
            if not symbol:
                return None
            
            df = self.get_historical_data(symbol, days=window + 10)
            if df.empty or len(df) < window:
                return None
            
            ma = df['Close'].rolling(window=window).mean().iloc[-1]
            logger.info(f"Moving average ({window}d) for {symbol}: ${ma}")
            return float(ma)
        
        except Exception as e:
            logger.error(f"Error calculating moving average for {symbol}: {e}")
            return None

stock_service = StockService()
