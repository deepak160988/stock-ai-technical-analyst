import yfinance as yf
import pandas as pd
import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

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
    
    def get_historical_data(self, symbol: str, days: int = 365) -> pd.DataFrame:
        """Get historical stock data"""
        try:
            if not symbol:
                return pd.DataFrame()
            
            # Check cache first
            cache_key = f"{symbol}_{days}"
            if cache_key in self.cache:
                logger.info(f"Using cached data for {symbol}")
                return self.cache[cache_key]
            
            # Fetch data from yfinance
            ticker = yf.Ticker(symbol)
            period = f"{days}d"
            df = ticker.history(period=period)
            
            if df.empty:
                logger.warning(f"No data found for symbol {symbol}")
                return pd.DataFrame()
            
            # Cache the data
            self.cache[cache_key] = df
            logger.info(f"Retrieved {len(df)} rows of data for {symbol}")
            return df
        
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
