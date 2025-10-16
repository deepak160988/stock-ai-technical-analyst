"""
Technical indicators calculation module
"""
import pandas as pd
import numpy as np
from ta import momentum, trend, volatility, volume
import pandas_ta as ta_lib
from typing import Dict, Any, List


class TechnicalIndicators:
    """
    Calculate various technical indicators for stock analysis
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize TechnicalIndicators with stock data
        
        Args:
            data: DataFrame with OHLCV data
        """
        self.data = data.copy()
        
    def add_all_indicators(self) -> pd.DataFrame:
        """
        Add all common technical indicators to the data
        
        Returns:
            DataFrame with all indicators
        """
        self.add_moving_averages()
        self.add_rsi()
        self.add_macd()
        self.add_bollinger_bands()
        self.add_stochastic()
        self.add_atr()
        self.add_obv()
        self.add_adx()
        
        return self.data
    
    def add_moving_averages(self, periods: List[int] = [20, 50, 200]) -> pd.DataFrame:
        """
        Add Simple Moving Averages (SMA) and Exponential Moving Averages (EMA)
        
        Args:
            periods: List of periods for moving averages
            
        Returns:
            DataFrame with moving averages
        """
        for period in periods:
            self.data[f'SMA_{period}'] = self.data['Close'].rolling(window=period).mean()
            self.data[f'EMA_{period}'] = self.data['Close'].ewm(span=period, adjust=False).mean()
        
        return self.data
    
    def add_rsi(self, period: int = 14) -> pd.DataFrame:
        """
        Add Relative Strength Index (RSI)
        
        Args:
            period: RSI period
            
        Returns:
            DataFrame with RSI
        """
        rsi_indicator = momentum.RSIIndicator(close=self.data['Close'], window=period)
        self.data['RSI'] = rsi_indicator.rsi()
        
        return self.data
    
    def add_macd(self, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        """
        Add MACD (Moving Average Convergence Divergence)
        
        Args:
            fast: Fast period
            slow: Slow period
            signal: Signal period
            
        Returns:
            DataFrame with MACD indicators
        """
        macd = trend.MACD(close=self.data['Close'], window_fast=fast, window_slow=slow, window_sign=signal)
        self.data['MACD'] = macd.macd()
        self.data['MACD_Signal'] = macd.macd_signal()
        self.data['MACD_Diff'] = macd.macd_diff()
        
        return self.data
    
    def add_bollinger_bands(self, period: int = 20, std_dev: int = 2) -> pd.DataFrame:
        """
        Add Bollinger Bands
        
        Args:
            period: Moving average period
            std_dev: Standard deviation multiplier
            
        Returns:
            DataFrame with Bollinger Bands
        """
        bb = volatility.BollingerBands(close=self.data['Close'], window=period, window_dev=std_dev)
        self.data['BB_High'] = bb.bollinger_hband()
        self.data['BB_Mid'] = bb.bollinger_mavg()
        self.data['BB_Low'] = bb.bollinger_lband()
        self.data['BB_Width'] = bb.bollinger_wband()
        
        return self.data
    
    def add_stochastic(self, period: int = 14, smooth_k: int = 3, smooth_d: int = 3) -> pd.DataFrame:
        """
        Add Stochastic Oscillator
        
        Args:
            period: Stochastic period
            smooth_k: K smoothing period
            smooth_d: D smoothing period
            
        Returns:
            DataFrame with Stochastic indicators
        """
        stoch = momentum.StochasticOscillator(
            high=self.data['High'],
            low=self.data['Low'],
            close=self.data['Close'],
            window=period,
            smooth_window=smooth_k
        )
        self.data['Stoch_K'] = stoch.stoch()
        self.data['Stoch_D'] = stoch.stoch_signal()
        
        return self.data
    
    def add_atr(self, period: int = 14) -> pd.DataFrame:
        """
        Add Average True Range (ATR)
        
        Args:
            period: ATR period
            
        Returns:
            DataFrame with ATR
        """
        atr = volatility.AverageTrueRange(
            high=self.data['High'],
            low=self.data['Low'],
            close=self.data['Close'],
            window=period
        )
        self.data['ATR'] = atr.average_true_range()
        
        return self.data
    
    def add_obv(self) -> pd.DataFrame:
        """
        Add On-Balance Volume (OBV)
        
        Returns:
            DataFrame with OBV
        """
        obv_indicator = volume.OnBalanceVolumeIndicator(
            close=self.data['Close'],
            volume=self.data['Volume']
        )
        self.data['OBV'] = obv_indicator.on_balance_volume()
        
        return self.data
    
    def add_adx(self, period: int = 14) -> pd.DataFrame:
        """
        Add Average Directional Index (ADX)
        
        Args:
            period: ADX period
            
        Returns:
            DataFrame with ADX
        """
        adx = trend.ADXIndicator(
            high=self.data['High'],
            low=self.data['Low'],
            close=self.data['Close'],
            window=period
        )
        self.data['ADX'] = adx.adx()
        self.data['ADX_Pos'] = adx.adx_pos()
        self.data['ADX_Neg'] = adx.adx_neg()
        
        return self.data
    
    def get_latest_values(self) -> Dict[str, float]:
        """
        Get the latest values of all indicators
        
        Returns:
            Dictionary with latest indicator values
        """
        latest = {}
        
        # Get the last row
        last_row = self.data.iloc[-1]
        
        # Convert to dictionary, excluding OHLCV
        for col in self.data.columns:
            if col not in ['Open', 'High', 'Low', 'Close', 'Volume']:
                latest[col] = last_row[col]
        
        return latest
    
    def get_indicator_summary(self) -> Dict[str, Any]:
        """
        Get a summary of key indicators with interpretations
        
        Returns:
            Dictionary with indicator summary
        """
        latest = self.get_latest_values()
        
        summary = {
            "trend": {
                "SMA_20": latest.get('SMA_20'),
                "SMA_50": latest.get('SMA_50'),
                "SMA_200": latest.get('SMA_200'),
                "EMA_20": latest.get('EMA_20'),
                "ADX": latest.get('ADX'),
            },
            "momentum": {
                "RSI": latest.get('RSI'),
                "MACD": latest.get('MACD'),
                "MACD_Signal": latest.get('MACD_Signal'),
                "Stoch_K": latest.get('Stoch_K'),
                "Stoch_D": latest.get('Stoch_D'),
            },
            "volatility": {
                "BB_Width": latest.get('BB_Width'),
                "ATR": latest.get('ATR'),
            },
            "volume": {
                "OBV": latest.get('OBV'),
            }
        }
        
        return summary
