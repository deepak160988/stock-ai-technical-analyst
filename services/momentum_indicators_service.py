import pandas as pd
import numpy as np
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

class MomentumIndicatorsService:
    @staticmethod
    def calculate_stochastic(prices: List[float], window: int = 14, smooth_k: int = 3, smooth_d: int = 3) -> Tuple[List[float], List[float]]:
        try:
            if len(prices) < window:
                return [], []
            k_line = []
            for i in range(window - 1, len(prices)):
                lowest_low = min(prices[i-window+1:i+1])
                highest_high = max(prices[i-window+1:i+1])
                if highest_high - lowest_low == 0:
                    k_value = 50
                else:
                    k_value = ((prices[i] - lowest_low) / (highest_high - lowest_low)) * 100
                k_line.append(k_value)
            if len(k_line) < smooth_k:
                return k_line, []
            k_smooth = pd.Series(k_line).rolling(window=smooth_k).mean().tolist()
            if len(k_smooth) < smooth_d:
                return k_smooth, []
            d_line = pd.Series(k_smooth).rolling(window=smooth_d).mean().tolist()
            logger.info(f"Calculated Stochastic with {len(k_smooth)} K values and {len(d_line)} D values")
            return k_smooth, d_line
        except Exception as e:
            logger.error(f"Error calculating Stochastic: {str(e)}")
            return [], []
    
    @staticmethod
    def calculate_williams_r(highs: List[float], lows: List[float], closes: List[float], window: int = 14) -> List[float]:
        try:
            if len(closes) < window:
                return []
            williams_r = []
            for i in range(window - 1, len(closes)):
                highest_high = max(highs[i-window+1:i+1])
                lowest_low = min(lows[i-window+1:i+1])
                if highest_high - lowest_low == 0:
                    wr_value = -50
                else:
                    wr_value = -100 * ((highest_high - closes[i]) / (highest_high - lowest_low))
                williams_r.append(wr_value)
            logger.info(f"Calculated Williams %R with {len(williams_r)} data points")
            return williams_r
        except Exception as e:
            logger.error(f"Error calculating Williams %R: {str(e)}")
            return []
    
    @staticmethod
    def calculate_roc(prices: List[float], window: int = 12) -> List[float]:
        try:
            if len(prices) < window + 1:
                return []
            roc = []
            for i in range(window, len(prices)):
                if prices[i - window] == 0:
                    roc_value = 0
                else:
                    roc_value = ((prices[i] - prices[i - window]) / prices[i - window]) * 100
                roc.append(roc_value)
            logger.info(f"Calculated ROC with {len(roc)} data points")
            return roc
        except Exception as e:
            logger.error(f"Error calculating ROC: {str(e)}")
            return []
    
    @staticmethod
    def calculate_momentum(prices: List[float], window: int = 12) -> List[float]:
        try:
            if len(prices) < window + 1:
                return []
            momentum = []
            for i in range(window, len(prices)):
                momentum_value = prices[i] - prices[i - window]
                momentum.append(momentum_value)
            logger.info(f"Calculated Momentum with {len(momentum)} data points")
            return momentum
        except Exception as e:
            logger.error(f"Error calculating Momentum: {str(e)}")
            return []
    
    @staticmethod
    def calculate_cci(highs: List[float], lows: List[float], closes: List[float], window: int = 20) -> List[float]:
        try:
            if len(closes) < window:
                return []
            cci = []
            for i in range(window - 1, len(closes)):
                typical_price = (highs[i] + lows[i] + closes[i]) / 3
                sma = sum([(highs[j] + lows[j] + closes[j]) / 3 for j in range(i-window+1, i+1)]) / window
                mad = sum([abs((highs[j] + lows[j] + closes[j]) / 3 - sma) for j in range(i-window+1, i+1)]) / window
                if mad == 0:
                    cci_value = 0
                else:
                    cci_value = (typical_price - sma) / (0.015 * mad)
                cci.append(cci_value)
            logger.info(f"Calculated CCI with {len(cci)} data points")
            return cci
        except Exception as e:
            logger.error(f"Error calculating CCI: {str(e)}")
            return []

momentum_indicators_service = MomentumIndicatorsService()