"""
Visualization module for creating charts and graphs
"""
import matplotlib.pyplot as plt
import mplfinance as mpf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Optional, List, Dict, Any
import os


class ChartVisualizer:
    """
    Create various charts for stock technical analysis
    """
    
    def __init__(self, data: pd.DataFrame, symbol: str):
        """
        Initialize ChartVisualizer
        
        Args:
            data: DataFrame with stock data and indicators
            symbol: Stock symbol
        """
        self.data = data
        self.symbol = symbol
        
    def plot_candlestick(self, output_file: Optional[str] = None, show: bool = True) -> None:
        """
        Create candlestick chart with volume
        
        Args:
            output_file: Path to save the chart
            show: Whether to display the chart
        """
        # Prepare data for mplfinance
        plot_data = self.data[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
        
        # Create the plot
        kwargs = dict(
            type='candle',
            volume=True,
            title=f'{self.symbol} - Candlestick Chart',
            style='charles',
            figsize=(14, 8)
        )
        
        if output_file:
            kwargs['savefig'] = output_file
        
        mpf.plot(plot_data, **kwargs)
        
    def plot_with_indicators(self, 
                           indicators: List[str] = None,
                           output_file: Optional[str] = None) -> None:
        """
        Create interactive chart with technical indicators using Plotly
        
        Args:
            indicators: List of indicator names to plot
            output_file: Path to save the HTML chart
        """
        if indicators is None:
            indicators = ['SMA_20', 'SMA_50', 'RSI', 'MACD']
        
        # Create subplots
        rows = 1 + len([i for i in indicators if i in ['RSI', 'MACD', 'Stoch_K', 'ADX', 'OBV']])
        subplot_titles = [f'{self.symbol} Price'] + [i for i in indicators if i in ['RSI', 'MACD', 'Stoch_K', 'ADX', 'OBV']]
        
        fig = make_subplots(
            rows=min(rows, 4), cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=subplot_titles,
            row_heights=[0.5] + [0.2] * (min(rows, 4) - 1)
        )
        
        # Candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=self.data.index,
                open=self.data['Open'],
                high=self.data['High'],
                low=self.data['Low'],
                close=self.data['Close'],
                name='Price'
            ),
            row=1, col=1
        )
        
        # Add moving averages to main chart
        for indicator in indicators:
            if indicator.startswith('SMA') or indicator.startswith('EMA'):
                if indicator in self.data.columns:
                    fig.add_trace(
                        go.Scatter(
                            x=self.data.index,
                            y=self.data[indicator],
                            name=indicator,
                            line=dict(width=1.5)
                        ),
                        row=1, col=1
                    )
        
        # Add Bollinger Bands if available
        if 'BB_High' in self.data.columns and 'BB_Low' in self.data.columns:
            fig.add_trace(
                go.Scatter(
                    x=self.data.index,
                    y=self.data['BB_High'],
                    name='BB Upper',
                    line=dict(color='gray', width=1, dash='dash')
                ),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(
                    x=self.data.index,
                    y=self.data['BB_Low'],
                    name='BB Lower',
                    line=dict(color='gray', width=1, dash='dash'),
                    fill='tonexty',
                    fillcolor='rgba(128, 128, 128, 0.1)'
                ),
                row=1, col=1
            )
        
        current_row = 2
        
        # Add RSI
        if 'RSI' in indicators and 'RSI' in self.data.columns:
            fig.add_trace(
                go.Scatter(
                    x=self.data.index,
                    y=self.data['RSI'],
                    name='RSI',
                    line=dict(color='purple')
                ),
                row=current_row, col=1
            )
            # Add overbought/oversold lines
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=current_row, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=current_row, col=1)
            current_row += 1
        
        # Add MACD
        if 'MACD' in indicators and 'MACD' in self.data.columns and current_row <= min(rows, 4):
            fig.add_trace(
                go.Scatter(
                    x=self.data.index,
                    y=self.data['MACD'],
                    name='MACD',
                    line=dict(color='blue')
                ),
                row=current_row, col=1
            )
            if 'MACD_Signal' in self.data.columns:
                fig.add_trace(
                    go.Scatter(
                        x=self.data.index,
                        y=self.data['MACD_Signal'],
                        name='MACD Signal',
                        line=dict(color='orange')
                    ),
                    row=current_row, col=1
                )
            if 'MACD_Diff' in self.data.columns:
                fig.add_trace(
                    go.Bar(
                        x=self.data.index,
                        y=self.data['MACD_Diff'],
                        name='MACD Histogram',
                        marker_color='green'
                    ),
                    row=current_row, col=1
                )
            current_row += 1
        
        # Update layout
        fig.update_layout(
            title=f'{self.symbol} Technical Analysis',
            xaxis_title='Date',
            height=800,
            showlegend=True,
            template='plotly_white'
        )
        
        fig.update_xaxes(rangeslider_visible=False)
        
        if output_file:
            fig.write_html(output_file)
        else:
            fig.show()
    
    def plot_comparison(self, 
                       other_data: Dict[str, pd.DataFrame],
                       output_file: Optional[str] = None) -> None:
        """
        Compare multiple stocks on the same chart
        
        Args:
            other_data: Dictionary of {symbol: DataFrame} for comparison
            output_file: Path to save the HTML chart
        """
        fig = go.Figure()
        
        # Normalize prices to percentage change
        base_price = self.data['Close'].iloc[0]
        normalized = (self.data['Close'] / base_price - 1) * 100
        
        fig.add_trace(
            go.Scatter(
                x=self.data.index,
                y=normalized,
                name=self.symbol,
                line=dict(width=2)
            )
        )
        
        for symbol, data in other_data.items():
            if not data.empty:
                base = data['Close'].iloc[0]
                norm = (data['Close'] / base - 1) * 100
                fig.add_trace(
                    go.Scatter(
                        x=data.index,
                        y=norm,
                        name=symbol,
                        line=dict(width=2)
                    )
                )
        
        fig.update_layout(
            title='Stock Price Comparison (% Change)',
            xaxis_title='Date',
            yaxis_title='% Change',
            height=600,
            template='plotly_white',
            hovermode='x unified'
        )
        
        if output_file:
            fig.write_html(output_file)
        else:
            fig.show()
    
    def create_dashboard(self, output_file: str = 'dashboard.html') -> None:
        """
        Create a comprehensive dashboard with multiple charts
        
        Args:
            output_file: Path to save the HTML dashboard
        """
        from plotly.subplots import make_subplots
        
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                'Price & Volume', 'RSI',
                'MACD', 'Bollinger Bands',
                'Stochastic', 'ADX'
            ),
            specs=[
                [{"secondary_y": True}, {}],
                [{}, {}],
                [{}, {}]
            ],
            vertical_spacing=0.1,
            horizontal_spacing=0.1
        )
        
        # Price and Volume
        fig.add_trace(
            go.Candlestick(
                x=self.data.index,
                open=self.data['Open'],
                high=self.data['High'],
                low=self.data['Low'],
                close=self.data['Close'],
                name='Price'
            ),
            row=1, col=1, secondary_y=False
        )
        
        fig.add_trace(
            go.Bar(
                x=self.data.index,
                y=self.data['Volume'],
                name='Volume',
                marker_color='lightblue',
                opacity=0.5
            ),
            row=1, col=1, secondary_y=True
        )
        
        # RSI
        if 'RSI' in self.data.columns:
            fig.add_trace(
                go.Scatter(x=self.data.index, y=self.data['RSI'], name='RSI'),
                row=1, col=2
            )
        
        # MACD
        if 'MACD' in self.data.columns:
            fig.add_trace(
                go.Scatter(x=self.data.index, y=self.data['MACD'], name='MACD'),
                row=2, col=1
            )
            if 'MACD_Signal' in self.data.columns:
                fig.add_trace(
                    go.Scatter(x=self.data.index, y=self.data['MACD_Signal'], name='Signal'),
                    row=2, col=1
                )
        
        # Bollinger Bands
        if all(col in self.data.columns for col in ['BB_High', 'BB_Mid', 'BB_Low']):
            fig.add_trace(
                go.Scatter(x=self.data.index, y=self.data['BB_High'], name='BB Upper'),
                row=2, col=2
            )
            fig.add_trace(
                go.Scatter(x=self.data.index, y=self.data['BB_Mid'], name='BB Mid'),
                row=2, col=2
            )
            fig.add_trace(
                go.Scatter(x=self.data.index, y=self.data['BB_Low'], name='BB Lower'),
                row=2, col=2
            )
        
        # Stochastic
        if 'Stoch_K' in self.data.columns:
            fig.add_trace(
                go.Scatter(x=self.data.index, y=self.data['Stoch_K'], name='%K'),
                row=3, col=1
            )
            if 'Stoch_D' in self.data.columns:
                fig.add_trace(
                    go.Scatter(x=self.data.index, y=self.data['Stoch_D'], name='%D'),
                    row=3, col=1
                )
        
        # ADX
        if 'ADX' in self.data.columns:
            fig.add_trace(
                go.Scatter(x=self.data.index, y=self.data['ADX'], name='ADX'),
                row=3, col=2
            )
        
        fig.update_layout(
            height=1200,
            title_text=f"{self.symbol} - Technical Analysis Dashboard",
            showlegend=True
        )
        
        fig.write_html(output_file)
