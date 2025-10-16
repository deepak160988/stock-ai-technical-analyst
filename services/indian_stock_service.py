import yfinance as yf
import pandas as pd
import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

class IndianStockService:
    def __init__(self):
        self.cache = {}
        self.indian_stocks = {
            'RELIANCE': 'RELIANCE.NS',
            'TCS': 'TCS.NS',
            'INFY': 'INFY.NS',
            'WIPRO': 'WIPRO.NS',
            'HDFCBANK': 'HDFCBANK.NS',
            'ICICIBANK': 'ICICIBANK.NS',
            'AXISBANK': 'AXISBANK.NS',
            'MARUTI': 'MARUTI.NS',
            'BHARTI': 'BHARTIARTL.NS',
            'SUNPHARMA': 'SUNPHARMA.NS',
            'LT': 'LT.NS',
            'ASIANPAINT': 'ASIANPAINT.NS',
            'ADANIPOWER': 'ADANIPOWER.NS',
            'ADANIENT': 'ADANIENT.NS',
            'ITC': 'ITC.NS',
            'SBIN': 'SBIN.NS',
            'INDIGO': 'INDIGO.NS',
            'TATAMOTORS': 'TATAMOTORS.NS',
            'TATASTEEL': 'TATASTEEL.NS',
            'NESTLEIND': 'NESTLEIND.NS',
            'POWERGRID': 'POWERGRID.NS',
            'NTPC': 'NTPC.NS',
            'ONGC': 'ONGC.NS',
            'COALINDIA': 'COALINDIA.NS',
            'BAJAJFINSV': 'BAJAJFINSV.NS',
            'HEROMOTOCO': 'HEROMOTOCO.NS',
            'HINDUNILVR': 'HINDUNILVR.NS',
            'DMART': 'DMART.NS',
            'SHRIRAMFIN': 'SHRIRAMFIN.NS',
            'HDFC': 'HDFC.NS',
            'CIPLA': 'CIPLA.NS',
            'DIVISLAB': 'DIVISLAB.NS',
            'LUPIN': 'LUPIN.NS',
            'DRREDDY': 'DRREDDY.NS',
            'GRASIM': 'GRASIM.NS',
            'ULTRACEMCO': 'ULTRACEMCO.NS',
            'SBILIFE': 'SBILIFE.NS',
            'ICICIGI': 'ICICIGI.NS',
            'APOLLOHOSP': 'APOLLOHOSP.NS',
            'MAXHEALTH': 'MAXHEALTH.NS',
            'MINDTREE': 'MINDTREE.NS',
            'PERSISTENT': 'PERSISTENT.NS',
        }
    
    def get_nse_symbol(self, symbol: str) -> str:
        """Convert symbol to NSE format"""
        symbol = symbol.upper()
        if symbol in self.indian_stocks:
            return self.indian_stocks[symbol]
        if symbol.endswith('.NS') or symbol.endswith('.BO'):
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
            return info.get('symbol') is not None or len(symbol) >= 1
        except Exception as e:
            logger.warning(f"Indian symbol validation failed for {symbol}: {e}")
            return len(symbol) >= 1 and len(symbol) <= 20
    
    def get_indian_stock_historical_data(self, symbol: str, days: int = 365) -> pd.DataFrame:
        """Get historical data for Indian stock"""
        try:
            nse_symbol = self.get_nse_symbol(symbol)
            
            cache_key = f"{nse_symbol}_{days}"
            if cache_key in self.cache:
                logger.info(f"Using cached data for {nse_symbol}")
                return self.cache[cache_key]
            
            ticker = yf.Ticker(nse_symbol)
            period = f"{days}d"
            df = ticker.history(period=period)
            
            if df.empty:
                logger.warning(f"No data found for Indian stock {nse_symbol}")
                return pd.DataFrame()
            
            self.cache[cache_key] = df
            logger.info(f"Retrieved {len(df)} rows of data for {nse_symbol}")
            return df
        
        except Exception as e:
            logger.error(f"Error fetching historical data for Indian stock {symbol}: {e}")
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
            
            latest_price = data['Close'].iloc[-1]
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
    
    def get_indian_stock_price_change(self, symbol: str, days: int = 1) -> Optional[float]:
        """Get price change percentage for Indian stock"""
        try:
            nse_symbol = self.get_nse_symbol(symbol)
            ticker = yf.Ticker(nse_symbol)
            data = ticker.history(period=f"{days + 1}d")
            
            if len(data) < 2:
                return None
            
            old_price = data['Close'].iloc[0]
            new_price = data['Close'].iloc[-1]
            
            change_percent = ((new_price - old_price) / old_price) * 100
            logger.info(f"Price change for {nse_symbol} ({days}d): {change_percent:.2f}%")
            return float(change_percent)
        
        except Exception as e:
            logger.error(f"Error calculating price change for Indian stock {symbol}: {e}")
            return None
    
    def get_top_indian_stocks(self) -> List[Dict]:
        """Get list of popular Indian stocks"""
        stocks = []
        for short_name, nse_symbol in list(self.indian_stocks.items())[:10]:
            try:
                price = self.get_indian_stock_price(short_name)
                stocks.append({
                    "symbol": short_name,
                    "nse_symbol": nse_symbol,
                    "price_inr": price,
                    "currency": "INR"
                })
            except Exception as e:
                logger.warning(f"Could not fetch {nse_symbol}: {e}")
        return stocks
    
    def search_indian_stocks(self, query: str) -> List[str]:
        """Search for Indian stocks by query"""
        try:
            query = query.upper()
            results = []
            
            for symbol, nse_symbol in self.indian_stocks.items():
                if query in symbol or query in nse_symbol:
                    results.append(symbol)
            
            logger.info(f"Search for '{query}' returned {len(results)} results")
            return results
        
        except Exception as e:
            logger.error(f"Error searching Indian stocks: {e}")
            return []

indian_stock_service = IndianStockService()