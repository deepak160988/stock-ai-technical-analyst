"""
Stock data fetching and basic analysis module
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


class StockAnalyzer:
    """
    Main class for fetching and analyzing stock data
    """
    
    def __init__(self, symbol: str):
        """
        Initialize StockAnalyzer with a stock symbol
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
        """
        self.symbol = symbol.upper()
        self.ticker = yf.Ticker(self.symbol)
        self.data = None
        self.info = None
        
    def fetch_data(self, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
        """
        Fetch historical stock data
        
        Args:
            period: Data period (e.g., '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max')
            interval: Data interval (e.g., '1m', '5m', '15m', '1d', '1wk', '1mo')
            
        Returns:
            DataFrame with stock data
        """
        self.data = self.ticker.history(period=period, interval=interval)
        return self.data
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get stock information and metadata
        
        Returns:
            Dictionary with stock info
        """
        try:
            self.info = self.ticker.info
            return self.info
        except Exception as e:
            return {"error": str(e)}
    
    def get_current_price(self) -> float:
        """
        Get current stock price
        
        Returns:
            Current price
        """
        if self.data is None or self.data.empty:
            self.fetch_data(period="1d", interval="1m")
        
        return self.data['Close'].iloc[-1] if not self.data.empty else 0.0
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get stock summary with key metrics
        
        Returns:
            Dictionary with summary information
        """
        if self.data is None or self.data.empty:
            self.fetch_data()
        
        if self.info is None:
            self.get_info()
        
        summary = {
            "symbol": self.symbol,
            "current_price": self.get_current_price(),
            "volume": self.data['Volume'].iloc[-1] if not self.data.empty else 0,
            "avg_volume": self.data['Volume'].mean() if not self.data.empty else 0,
            "high_52w": self.data['High'].max() if not self.data.empty else 0,
            "low_52w": self.data['Low'].min() if not self.data.empty else 0,
            "price_change_pct": ((self.data['Close'].iloc[-1] - self.data['Close'].iloc[0]) / 
                                self.data['Close'].iloc[0] * 100) if not self.data.empty and len(self.data) > 1 else 0,
        }
        
        # Add info data if available
        if self.info and not self.info.get("error"):
            summary.update({
                "company_name": self.info.get("longName", "N/A"),
                "sector": self.info.get("sector", "N/A"),
                "industry": self.info.get("industry", "N/A"),
                "market_cap": self.info.get("marketCap", "N/A"),
            })
        
        return summary
    
    def get_ohlcv(self) -> pd.DataFrame:
        """
        Get OHLCV (Open, High, Low, Close, Volume) data
        
        Returns:
            DataFrame with OHLCV data
        """
        if self.data is None or self.data.empty:
            self.fetch_data()
        
        return self.data[['Open', 'High', 'Low', 'Close', 'Volume']]
