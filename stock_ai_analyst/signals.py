"""
Buy/Sell signal generation module
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
from datetime import datetime


class SignalGenerator:
    """
    Generate buy/sell signals based on technical indicators
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize SignalGenerator
        
        Args:
            data: DataFrame with stock data and technical indicators
        """
        self.data = data.copy()
        self.signals = []
        
    def generate_all_signals(self) -> List[Dict[str, Any]]:
        """
        Generate all types of signals
        
        Returns:
            List of signal dictionaries
        """
        self.signals = []
        
        # Generate various signals
        self.moving_average_crossover()
        self.rsi_signals()
        self.macd_signals()
        self.bollinger_band_signals()
        self.stochastic_signals()
        self.trend_strength_signals()
        
        return self.signals
    
    def moving_average_crossover(self) -> None:
        """
        Generate signals based on moving average crossovers
        """
        if 'SMA_20' not in self.data.columns or 'SMA_50' not in self.data.columns:
            return
        
        # Golden Cross (bullish) - 20 crosses above 50
        # Death Cross (bearish) - 20 crosses below 50
        
        for i in range(1, len(self.data)):
            prev_20 = self.data['SMA_20'].iloc[i-1]
            curr_20 = self.data['SMA_20'].iloc[i]
            prev_50 = self.data['SMA_50'].iloc[i-1]
            curr_50 = self.data['SMA_50'].iloc[i]
            
            if pd.notna(prev_20) and pd.notna(curr_20) and pd.notna(prev_50) and pd.notna(curr_50):
                # Golden Cross
                if prev_20 <= prev_50 and curr_20 > curr_50:
                    self.signals.append({
                        'date': self.data.index[i],
                        'type': 'BUY',
                        'signal': 'Golden Cross',
                        'description': 'SMA 20 crossed above SMA 50',
                        'strength': 'STRONG',
                        'price': self.data['Close'].iloc[i]
                    })
                
                # Death Cross
                elif prev_20 >= prev_50 and curr_20 < curr_50:
                    self.signals.append({
                        'date': self.data.index[i],
                        'type': 'SELL',
                        'signal': 'Death Cross',
                        'description': 'SMA 20 crossed below SMA 50',
                        'strength': 'STRONG',
                        'price': self.data['Close'].iloc[i]
                    })
    
    def rsi_signals(self) -> None:
        """
        Generate signals based on RSI (oversold/overbought)
        """
        if 'RSI' not in self.data.columns:
            return
        
        for i in range(1, len(self.data)):
            prev_rsi = self.data['RSI'].iloc[i-1]
            curr_rsi = self.data['RSI'].iloc[i]
            
            if pd.notna(prev_rsi) and pd.notna(curr_rsi):
                # Oversold -> Buy signal
                if prev_rsi <= 30 and curr_rsi > 30:
                    self.signals.append({
                        'date': self.data.index[i],
                        'type': 'BUY',
                        'signal': 'RSI Oversold Recovery',
                        'description': f'RSI moved above 30 (oversold recovery)',
                        'strength': 'MEDIUM',
                        'price': self.data['Close'].iloc[i]
                    })
                
                # Overbought -> Sell signal
                elif prev_rsi >= 70 and curr_rsi < 70:
                    self.signals.append({
                        'date': self.data.index[i],
                        'type': 'SELL',
                        'signal': 'RSI Overbought Correction',
                        'description': f'RSI moved below 70 (overbought correction)',
                        'strength': 'MEDIUM',
                        'price': self.data['Close'].iloc[i]
                    })
    
    def macd_signals(self) -> None:
        """
        Generate signals based on MACD crossovers
        """
        if 'MACD' not in self.data.columns or 'MACD_Signal' not in self.data.columns:
            return
        
        for i in range(1, len(self.data)):
            prev_macd = self.data['MACD'].iloc[i-1]
            curr_macd = self.data['MACD'].iloc[i]
            prev_signal = self.data['MACD_Signal'].iloc[i-1]
            curr_signal = self.data['MACD_Signal'].iloc[i]
            
            if all(pd.notna(x) for x in [prev_macd, curr_macd, prev_signal, curr_signal]):
                # Bullish crossover
                if prev_macd <= prev_signal and curr_macd > curr_signal:
                    self.signals.append({
                        'date': self.data.index[i],
                        'type': 'BUY',
                        'signal': 'MACD Bullish Crossover',
                        'description': 'MACD crossed above signal line',
                        'strength': 'STRONG',
                        'price': self.data['Close'].iloc[i]
                    })
                
                # Bearish crossover
                elif prev_macd >= prev_signal and curr_macd < curr_signal:
                    self.signals.append({
                        'date': self.data.index[i],
                        'type': 'SELL',
                        'signal': 'MACD Bearish Crossover',
                        'description': 'MACD crossed below signal line',
                        'strength': 'STRONG',
                        'price': self.data['Close'].iloc[i]
                    })
    
    def bollinger_band_signals(self) -> None:
        """
        Generate signals based on Bollinger Bands
        """
        if not all(col in self.data.columns for col in ['BB_High', 'BB_Low', 'Close']):
            return
        
        for i in range(1, len(self.data)):
            prev_close = self.data['Close'].iloc[i-1]
            curr_close = self.data['Close'].iloc[i]
            prev_bb_low = self.data['BB_Low'].iloc[i-1]
            curr_bb_low = self.data['BB_Low'].iloc[i]
            prev_bb_high = self.data['BB_High'].iloc[i-1]
            curr_bb_high = self.data['BB_High'].iloc[i]
            
            if all(pd.notna(x) for x in [prev_close, curr_close, prev_bb_low, curr_bb_low, prev_bb_high, curr_bb_high]):
                # Bounce from lower band (buy signal)
                if prev_close <= prev_bb_low and curr_close > curr_bb_low:
                    self.signals.append({
                        'date': self.data.index[i],
                        'type': 'BUY',
                        'signal': 'BB Lower Band Bounce',
                        'description': 'Price bounced from lower Bollinger Band',
                        'strength': 'MEDIUM',
                        'price': self.data['Close'].iloc[i]
                    })
                
                # Rejection from upper band (sell signal)
                elif prev_close >= prev_bb_high and curr_close < curr_bb_high:
                    self.signals.append({
                        'date': self.data.index[i],
                        'type': 'SELL',
                        'signal': 'BB Upper Band Rejection',
                        'description': 'Price rejected from upper Bollinger Band',
                        'strength': 'MEDIUM',
                        'price': self.data['Close'].iloc[i]
                    })
    
    def stochastic_signals(self) -> None:
        """
        Generate signals based on Stochastic Oscillator
        """
        if 'Stoch_K' not in self.data.columns or 'Stoch_D' not in self.data.columns:
            return
        
        for i in range(1, len(self.data)):
            prev_k = self.data['Stoch_K'].iloc[i-1]
            curr_k = self.data['Stoch_K'].iloc[i]
            prev_d = self.data['Stoch_D'].iloc[i-1]
            curr_d = self.data['Stoch_D'].iloc[i]
            
            if all(pd.notna(x) for x in [prev_k, curr_k, prev_d, curr_d]):
                # Bullish crossover in oversold region
                if prev_k <= prev_d and curr_k > curr_d and curr_k < 20:
                    self.signals.append({
                        'date': self.data.index[i],
                        'type': 'BUY',
                        'signal': 'Stochastic Bullish Crossover',
                        'description': 'Stochastic %K crossed above %D in oversold region',
                        'strength': 'STRONG',
                        'price': self.data['Close'].iloc[i]
                    })
                
                # Bearish crossover in overbought region
                elif prev_k >= prev_d and curr_k < curr_d and curr_k > 80:
                    self.signals.append({
                        'date': self.data.index[i],
                        'type': 'SELL',
                        'signal': 'Stochastic Bearish Crossover',
                        'description': 'Stochastic %K crossed below %D in overbought region',
                        'strength': 'STRONG',
                        'price': self.data['Close'].iloc[i]
                    })
    
    def trend_strength_signals(self) -> None:
        """
        Generate signals based on trend strength (ADX)
        """
        if 'ADX' not in self.data.columns:
            return
        
        # ADX > 25 indicates strong trend
        # Combined with directional indicators for buy/sell
        if 'ADX_Pos' in self.data.columns and 'ADX_Neg' in self.data.columns:
            for i in range(1, len(self.data)):
                adx = self.data['ADX'].iloc[i]
                adx_pos = self.data['ADX_Pos'].iloc[i]
                adx_neg = self.data['ADX_Neg'].iloc[i]
                
                if all(pd.notna(x) for x in [adx, adx_pos, adx_neg]) and adx > 25:
                    # Strong uptrend
                    if adx_pos > adx_neg and adx_pos > 25:
                        # Check if it's a new strong trend
                        prev_adx = self.data['ADX'].iloc[i-1]
                        if pd.notna(prev_adx) and prev_adx <= 25:
                            self.signals.append({
                                'date': self.data.index[i],
                                'type': 'BUY',
                                'signal': 'Strong Uptrend Emerging',
                                'description': f'ADX indicates strong uptrend forming',
                                'strength': 'STRONG',
                                'price': self.data['Close'].iloc[i]
                            })
                    
                    # Strong downtrend
                    elif adx_neg > adx_pos and adx_neg > 25:
                        prev_adx = self.data['ADX'].iloc[i-1]
                        if pd.notna(prev_adx) and prev_adx <= 25:
                            self.signals.append({
                                'date': self.data.index[i],
                                'type': 'SELL',
                                'signal': 'Strong Downtrend Emerging',
                                'description': f'ADX indicates strong downtrend forming',
                                'strength': 'STRONG',
                                'price': self.data['Close'].iloc[i]
                            })
    
    def get_latest_signals(self, n: int = 5) -> List[Dict[str, Any]]:
        """
        Get the most recent signals
        
        Args:
            n: Number of recent signals to return
            
        Returns:
            List of recent signals
        """
        if not self.signals:
            self.generate_all_signals()
        
        # Sort by date (most recent first)
        sorted_signals = sorted(self.signals, key=lambda x: x['date'], reverse=True)
        
        return sorted_signals[:n]
    
    def get_current_recommendation(self) -> Dict[str, Any]:
        """
        Get overall buy/sell recommendation based on all signals
        
        Returns:
            Dictionary with recommendation
        """
        if not self.signals:
            self.generate_all_signals()
        
        # Get signals from the last few days
        recent_signals = self.get_latest_signals(n=10)
        
        buy_score = 0
        sell_score = 0
        
        for signal in recent_signals:
            strength_multiplier = {'STRONG': 2, 'MEDIUM': 1, 'WEAK': 0.5}.get(signal['strength'], 1)
            
            if signal['type'] == 'BUY':
                buy_score += strength_multiplier
            elif signal['type'] == 'SELL':
                sell_score += strength_multiplier
        
        # Determine recommendation
        if buy_score > sell_score * 1.5:
            recommendation = 'STRONG BUY'
        elif buy_score > sell_score:
            recommendation = 'BUY'
        elif sell_score > buy_score * 1.5:
            recommendation = 'STRONG SELL'
        elif sell_score > buy_score:
            recommendation = 'SELL'
        else:
            recommendation = 'HOLD'
        
        return {
            'recommendation': recommendation,
            'buy_score': buy_score,
            'sell_score': sell_score,
            'recent_signals': recent_signals[:5],
            'confidence': abs(buy_score - sell_score) / max(buy_score + sell_score, 1) * 100
        }
