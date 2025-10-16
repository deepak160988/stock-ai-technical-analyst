import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class VolumeIndicatorsService:
    @staticmethod
    def calculate_obv(prices: List[float], volumes: List[int]) -> List[float]:
        try:
            if len(prices) != len(volumes) or len(prices) < 2:
                return []
            obv = [volumes[0]]
            for i in range(1, len(prices)):
                if prices[i] > prices[i-1]:
                    obv.append(obv[-1] + volumes[i])
                elif prices[i] < prices[i-1]:
                    obv.append(obv[-1] - volumes[i])
                else:
                    obv.append(obv[-1])
            logger.info(f"Calculated OBV with {len(obv)} data points")
            return obv
        except Exception as e:
            logger.error(f"Error calculating OBV: {str(e)}")
            return []
    
    @staticmethod
    def calculate_ad(highs: List[float], lows: List[float], closes: List[float], volumes: List[int]) -> List[float]:
        try:
            if len(highs) != len(lows) or len(lows) != len(closes) or len(closes) != len(volumes):
                return []
            if len(closes) < 1:
                return []
            ad = []
            cum_ad = 0
            for i in range(len(closes)):
                high_low_range = highs[i] - lows[i]
                if high_low_range == 0:
                    clv = 0
                else:
                    clv = ((closes[i] - lows[i]) - (highs[i] - closes[i])) / high_low_range
                ad_value = clv * volumes[i]
                cum_ad += ad_value
                ad.append(cum_ad)
            logger.info(f"Calculated A/D with {len(ad)} data points")
            return ad
        except Exception as e:
            logger.error(f"Error calculating A/D: {str(e)}")
            return []
    
    @staticmethod
    def calculate_mfi(highs: List[float], lows: List[float], closes: List[float], volumes: List[int], window: int = 14) -> List[float]:
        try:
            if len(closes) < window + 1:
                return []
            typical_prices = [(h + l + c) / 3 for h, l, c in zip(highs, lows, closes)]
            positive_mf = []
            negative_mf = []
            for i in range(1, len(typical_prices)):
                mf = typical_prices[i] * volumes[i]
                if typical_prices[i] > typical_prices[i-1]:
                    positive_mf.append(mf)
                    negative_mf.append(0)
                else:
                    positive_mf.append(0)
                    negative_mf.append(mf)
            mfi = []
            for i in range(window - 1, len(positive_mf)):
                pos_sum = sum(positive_mf[i-window+1:i+1])
                neg_sum = sum(negative_mf[i-window+1:i+1])
                if neg_sum == 0:
                    mfi_value = 100
                else:
                    mfi_value = 100 - (100 / (1 + pos_sum / neg_sum))
                mfi.append(mfi_value)
            logger.info(f"Calculated MFI with {len(mfi)} data points")
            return mfi
        except Exception as e:
            logger.error(f"Error calculating MFI: {str(e)}")
            return []

volume_indicators_service = VolumeIndicatorsService()