import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)

class IndicatorsService:
    """Service for calculating technical indicators"""
    
    def __init__(self):
        logger.info("Initializing IndicatorsService")
    
    def calculate_sma(self, prices: List[float], window: int = 20) -> List[float]:
        """Calculate Simple Moving Average"""
        try:
            df = pd.DataFrame({'price': prices})
            sma = df['price'].rolling(window=window, min_periods=1).mean()
            return sma.tolist()
        except Exception as e:
            logger.error(f"Error calculating SMA: {e}")
            return []
    
    def calculate_ema(self, prices: List[float], span: int = 20) -> List[float]:
        """Calculate Exponential Moving Average"""
        try:
            df = pd.DataFrame({'price': prices})
            ema = df['price'].ewm(span=span, adjust=False).mean()
            return ema.tolist()
        except Exception as e:
            logger.error(f"Error calculating EMA: {e}")
            return []
    
    def calculate_rsi(self, prices: List[float], window: int = 14) -> Tuple[List[float], List[bool], List[bool]]:
        """Calculate Relative Strength Index"""
        try:
            df = pd.DataFrame({'price': prices})
            delta = df['price'].diff()
            
            gain = (delta.where(delta > 0, 0)).rolling(window=window, min_periods=1).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=window, min_periods=1).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            overbought = (rsi > 70).tolist()
            oversold = (rsi < 30).tolist()
            
            return rsi.fillna(50).tolist(), overbought, oversold
        except Exception as e:
            logger.error(f"Error calculating RSI: {e}")
            return [], [], []
    
    def calculate_macd(self, prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[List[float], List[float], List[float]]:
        """Calculate MACD (Moving Average Convergence Divergence)"""
        try:
            df = pd.DataFrame({'price': prices})
            
            ema_fast = df['price'].ewm(span=fast, adjust=False).mean()
            ema_slow = df['price'].ewm(span=slow, adjust=False).mean()
            
            macd_line = ema_fast - ema_slow
            signal_line = macd_line.ewm(span=signal, adjust=False).mean()
            histogram = macd_line - signal_line
            
            return macd_line.tolist(), signal_line.tolist(), histogram.tolist()
        except Exception as e:
            logger.error(f"Error calculating MACD: {e}")
            return [], [], []
    
    def calculate_bollinger_bands(self, prices: List[float], window: int = 20, num_std: float = 2) -> Tuple[List[float], List[float], List[float]]:
        """Calculate Bollinger Bands"""
        try:
            df = pd.DataFrame({'price': prices})
            
            sma = df['price'].rolling(window=window, min_periods=1).mean()
            std = df['price'].rolling(window=window, min_periods=1).std()
            
            upper_band = sma + (std * num_std)
            lower_band = sma - (std * num_std)
            
            return upper_band.fillna(0).tolist(), sma.fillna(0).tolist(), lower_band.fillna(0).tolist()
        except Exception as e:
            logger.error(f"Error calculating Bollinger Bands: {e}")
            return [], [], []
    
    def calculate_stochastic(self, high: List[float], low: List[float], close: List[float], window: int = 14) -> Tuple[List[float], List[float]]:
        """Calculate Stochastic Oscillator"""
        try:
            df = pd.DataFrame({'high': high, 'low': low, 'close': close})
            
            lowest_low = df['low'].rolling(window=window, min_periods=1).min()
            highest_high = df['high'].rolling(window=window, min_periods=1).max()
            
            k = 100 * (df['close'] - lowest_low) / (highest_high - lowest_low)
            d = k.rolling(window=3, min_periods=1).mean()
            
            return k.fillna(50).tolist(), d.fillna(50).tolist()
        except Exception as e:
            logger.error(f"Error calculating Stochastic: {e}")
            return [], []
    
    def calculate_atr(self, high: List[float], low: List[float], close: List[float], window: int = 14) -> List[float]:
        """Calculate Average True Range"""
        try:
            df = pd.DataFrame({'high': high, 'low': low, 'close': close})
            
            high_low = df['high'] - df['low']
            high_close = abs(df['high'] - df['close'].shift())
            low_close = abs(df['low'] - df['close'].shift())
            
            true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
            atr = true_range.rolling(window=window, min_periods=1).mean()
            
            return atr.fillna(0).tolist()
        except Exception as e:
            logger.error(f"Error calculating ATR: {e}")
            return []
    
    def get_all_indicators(self, df: pd.DataFrame) -> Optional[Dict]:
        """Calculate all indicators from a DataFrame"""
        try:
            if df.empty:
                logger.warning("Empty DataFrame provided")
                return None
            
            prices = df['Close'].tolist()
            high = df['High'].tolist()
            low = df['Low'].tolist()
            
            # Calculate all indicators
            sma_20 = self.calculate_sma(prices, 20)
            sma_50 = self.calculate_sma(prices, 50)
            ema_20 = self.calculate_ema(prices, 20)
            ema_50 = self.calculate_ema(prices, 50)
            
            rsi_values, overbought, oversold = self.calculate_rsi(prices, 14)
            macd_line, signal_line, histogram = self.calculate_macd(prices)
            bb_upper, bb_middle, bb_lower = self.calculate_bollinger_bands(prices, 20)
            stoch_k, stoch_d = self.calculate_stochastic(high, low, prices, 14)
            atr = self.calculate_atr(high, low, prices, 14)
            
            # Get latest values
            indicators = {
                'sma_20': sma_20[-1] if sma_20 else None,
                'sma_50': sma_50[-1] if sma_50 else None,
                'ema_20': ema_20[-1] if ema_20 else None,
                'ema_50': ema_50[-1] if ema_50 else None,
                'rsi': rsi_values[-1] if rsi_values else None,
                'rsi_overbought': overbought[-1] if overbought else False,
                'rsi_oversold': oversold[-1] if oversold else False,
                'macd': macd_line[-1] if macd_line else None,
                'macd_signal': signal_line[-1] if signal_line else None,
                'macd_histogram': histogram[-1] if histogram else None,
                'bb_upper': bb_upper[-1] if bb_upper else None,
                'bb_middle': bb_middle[-1] if bb_middle else None,
                'bb_lower': bb_lower[-1] if bb_lower else None,
                'stochastic_k': stoch_k[-1] if stoch_k else None,
                'stochastic_d': stoch_d[-1] if stoch_d else None,
                'atr': atr[-1] if atr else None,
                'current_price': prices[-1] if prices else None,
            }
            
            # Fixed logging statement
            rsi_str = f"{indicators['rsi']:.2f}" if indicators['rsi'] is not None else "N/A"
            macd_str = f"{indicators['macd']:.2f}" if indicators['macd'] is not None else "N/A"
            logger.info(f"Calculated indicators: RSI={rsi_str}, MACD={macd_str}")
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error calculating all indicators: {e}")
            return None

# Create a singleton instance
indicators_service = IndicatorsService()