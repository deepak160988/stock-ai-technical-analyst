import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class TrendIndicatorsService:
    @staticmethod
    def calculate_adx(highs: List[float], lows: List[float], closes: List[float], window: int = 14) -> Tuple[List[float], List[float], List[float]]:
        try:
            if len(closes) < window + 1:
                return [], [], []
            tr = []
            for i in range(1, len(closes)):
                high_low = highs[i] - lows[i]
                high_close = abs(highs[i] - closes[i-1])
                low_close = abs(lows[i] - closes[i-1])
                tr_value = max(high_low, high_close, low_close)
                tr.append(tr_value)
            plus_dm = []
            minus_dm = []
            for i in range(1, len(highs)):
                up_move = highs[i] - highs[i-1]
                down_move = lows[i-1] - lows[i]
                if up_move > down_move and up_move > 0:
                    plus_dm.append(up_move)
                    minus_dm.append(0)
                elif down_move > up_move and down_move > 0:
                    plus_dm.append(0)
                    minus_dm.append(down_move)
                else:
                    plus_dm.append(0)
                    minus_dm.append(0)
            plus_di = []
            minus_di = []
            adx = []
            if len(tr) >= window:
                tr_sum = sum(tr[:window])
                plus_dm_sum = sum(plus_dm[:window])
                minus_dm_sum = sum(minus_dm[:window])
                for i in range(window - 1, len(tr)):
                    if i >= window:
                        tr_sum = tr_sum - tr[i-window] + tr[i]
                        plus_dm_sum = plus_dm_sum - plus_dm[i-window] + plus_dm[i]
                        minus_dm_sum = minus_dm_sum - minus_dm[i-window] + minus_dm[i]
                    if tr_sum != 0:
                        plus_di_val = 100 * (plus_dm_sum / tr_sum)
                        minus_di_val = 100 * (minus_dm_sum / tr_sum)
                    else:
                        plus_di_val = 0
                        minus_di_val = 0
                    plus_di.append(plus_di_val)
                    minus_di.append(minus_di_val)
                    di_sum = plus_di_val + minus_di_val
                    if di_sum != 0:
                        dx = 100 * abs(plus_di_val - minus_di_val) / di_sum
                    else:
                        dx = 0
                    if len(adx) < window:
                        adx.append(dx)
                    else:
                        adx_val = (adx[-1] * (window - 1) + dx) / window
                        adx.append(adx_val)
            logger.info(f"Calculated ADX with +DI: {len(plus_di)}, -DI: {len(minus_di)}, ADX: {len(adx)}")
            return adx, plus_di, minus_di
        except Exception as e:
            logger.error(f"Error calculating ADX: {str(e)}")
            return [], [], []
    
    @staticmethod
    def calculate_supertrend(highs: List[float], lows: List[float], closes: List[float], window: int = 10, multiplier: float = 3.0) -> Tuple[List[float], List[str]]:
        try:
            if len(closes) < window:
                return [], []
            hl2 = [(h + l) / 2 for h, l in zip(highs, lows)]
            atr_values = []
            for i in range(1, len(closes)):
                high_low = highs[i] - lows[i]
                high_close = abs(highs[i] - closes[i-1])
                low_close = abs(lows[i] - closes[i-1])
                tr = max(high_low, high_close, low_close)
                atr_values.append(tr)
            hl2_ma = pd.Series(hl2).rolling(window=window).mean().tolist()
            atr_ma = pd.Series(atr_values).rolling(window=window).mean().tolist()
            supertrend = []
            trend = []
            for i in range(len(hl2_ma) - len(atr_ma), len(hl2_ma)):
                idx = i - (len(hl2_ma) - len(atr_ma))
                if idx >= 0 and idx < len(atr_ma):
                    upper_band = hl2_ma[i] + (multiplier * atr_ma[idx])
                    lower_band = hl2_ma[i] - (multiplier * atr_ma[idx])
                    if closes[i] <= upper_band:
                        supertrend.append(upper_band)
                        trend.append("down")
                    else:
                        supertrend.append(lower_band)
                        trend.append("up")
            logger.info(f"Calculated Supertrend with {len(supertrend)} data points")
            return supertrend, trend
        except Exception as e:
            logger.error(f"Error calculating Supertrend: {str(e)}")
            return [], []
    
    @staticmethod
    def calculate_ichimoku(highs: List[float], lows: List[float], closes: List[float]) -> Dict[str, List[float]]:
        try:
            if len(closes) < 52:
                return {}
            tenkan = []
            for i in range(8, len(closes)):
                high_9 = max(highs[i-8:i+1])
                low_9 = min(lows[i-8:i+1])
                tenkan.append((high_9 + low_9) / 2)
            kijun = []
            for i in range(25, len(closes)):
                high_26 = max(highs[i-25:i+1])
                low_26 = min(lows[i-25:i+1])
                kijun.append((high_26 + low_26) / 2)
            senkou_a = [(tenkan[i] + kijun[i]) / 2 for i in range(len(kijun))]
            senkou_b = []
            for i in range(51, len(closes)):
                high_52 = max(highs[i-51:i+1])
                low_52 = min(lows[i-51:i+1])
                senkou_b.append((high_52 + low_52) / 2)
            chikou = closes[:-26] if len(closes) > 26 else []
            logger.info(f"Calculated Ichimoku with Tenkan: {len(tenkan)}, Kijun: {len(kijun)}")
            return {"tenkan": tenkan, "kijun": kijun, "senkou_a": senkou_a, "senkou_b": senkou_b, "chikou": chikou}
        except Exception as e:
            logger.error(f"Error calculating Ichimoku: {str(e)}")
            return {}

trend_indicators_service = TrendIndicatorsService()
