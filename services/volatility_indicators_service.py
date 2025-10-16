import numpy as np
import pandas as pd
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

class VolatilityIndicatorsService:
    @staticmethod
    def calculate_atr(highs: List[float], lows: List[float], closes: List[float], window: int = 14) -> List[float]:
        try:
            if len(closes) < window + 1:
                return []
            tr = []
            for i in range(1, len(closes)):
                high_low = highs[i] - lows[i]
                high_close = abs(highs[i] - closes[i-1])
                low_close = abs(lows[i] - closes[i-1])
                tr_value = max(high_low, high_close, low_close)
                tr.append(tr_value)
            atr = []
            if len(tr) >= window:
                atr.append(sum(tr[:window]) / window)
                for i in range(window, len(tr)):
                    atr_value = (atr[-1] * (window - 1) + tr[i]) / window
                    atr.append(atr_value)
            logger.info(f"Calculated ATR with {len(atr)} data points")
            return atr
        except Exception as e:
            logger.error(f"Error calculating ATR: {str(e)}")
            return []
    
    @staticmethod
    def calculate_historical_volatility(prices: List[float], window: int = 20) -> List[float]:
        try:
            if len(prices) < window + 1:
                return []
            volatility = []
            for i in range(window, len(prices)):
                returns = []
                for j in range(i - window, i):
                    if prices[j] != 0:
                        ret = (prices[j+1] - prices[j]) / prices[j]
                        returns.append(ret)
                if len(returns) > 0:
                    vol = np.std(returns)
                    volatility.append(vol * 100)
                else:
                    volatility.append(0)
            logger.info(f"Calculated Historical Volatility with {len(volatility)} data points")
            return volatility
        except Exception as e:
            logger.error(f"Error calculating Historical Volatility: {str(e)}")
            return []
    
    @staticmethod
    def calculate_keltner_channels(highs: List[float], lows: List[float], closes: List[float], window: int = 20, atr_multiplier: float = 2.0) -> Tuple[List[float], List[float], List[float]]:
        try:
            if len(closes) < window:
                return [], [], []
            ema = pd.Series(closes).ewm(span=window, adjust=False).mean().tolist()
            atr = VolatilityIndicatorsService.calculate_atr(highs, lows, closes, 10)
            if len(atr) == 0:
                return [], [], []
            ema_adjusted = ema[len(ema)-len(atr):]
            upper = [ema_adjusted[i] + (atr[i] * atr_multiplier) for i in range(len(atr))]
            lower = [ema_adjusted[i] - (atr[i] * atr_multiplier) for i in range(len(atr))]
            logger.info(f"Calculated Keltner Channels with {len(upper)} data points")
            return upper, ema_adjusted, lower
        except Exception as e:
            logger.error(f"Error calculating Keltner Channels: {str(e)}")
            return [], [], []
    
    @staticmethod
    def calculate_donchian_channels(highs: List[float], lows: List[float], window: int = 20) -> Tuple[List[float], List[float]]:
        try:
            if len(highs) < window or len(lows) < window:
                return [], []
            upper = []
            lower = []
            for i in range(window - 1, len(highs)):
                highest_high = max(highs[i-window+1:i+1])
                lowest_low = min(lows[i-window+1:i+1])
                upper.append(highest_high)
                lower.append(lowest_low)
            logger.info(f"Calculated Donchian Channels with {len(upper)} data points")
            return upper, lower
        except Exception as e:
            logger.error(f"Error calculating Donchian Channels: {str(e)}")
            return [], []

volatility_indicators_service = VolatilityIndicatorsService()
