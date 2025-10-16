#!/usr/bin/env python3
"""
Demo script with sample data (no network required)
This demonstrates all features using mock/sample data
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def create_sample_stock_data(symbol='DEMO', days=365):
    """
    Create sample stock data for demonstration
    
    Args:
        symbol: Stock symbol
        days: Number of days of data
        
    Returns:
        DataFrame with OHLCV data
    """
    # Create date range
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    
    # Generate realistic stock data
    np.random.seed(42)
    
    # Starting price
    base_price = 150.0
    
    # Create price series with trend and volatility
    trend = np.linspace(0, 30, days)  # Upward trend
    volatility = np.random.randn(days) * 3
    noise = np.random.randn(days) * 1
    
    close_prices = base_price + trend + volatility + noise
    
    # Generate OHLC from close
    data = pd.DataFrame(index=dates)
    data['Close'] = close_prices
    data['Open'] = close_prices + np.random.randn(days) * 0.5
    data['High'] = np.maximum(data['Open'], data['Close']) + np.abs(np.random.randn(days) * 0.3)
    data['Low'] = np.minimum(data['Open'], data['Close']) - np.abs(np.random.randn(days) * 0.3)
    data['Volume'] = (np.random.randint(50000000, 150000000, days) * 
                     (1 + np.random.randn(days) * 0.1))
    
    return data


def demo_technical_analysis():
    """
    Demonstrate technical analysis features
    """
    print("\n" + "="*70)
    print("DEMO: Stock Technical Analysis")
    print("="*70 + "\n")
    
    # Import modules
    from stock_ai_analyst import TechnicalIndicators, SignalGenerator
    
    # Create sample data
    print("Creating sample stock data...")
    data = create_sample_stock_data('DEMO', 365)
    print(f"✓ Generated {len(data)} days of sample data\n")
    
    # Show sample data
    print("Sample Data (last 5 days):")
    print(data[['Open', 'High', 'Low', 'Close', 'Volume']].tail())
    
    # Calculate technical indicators
    print("\n\nCalculating technical indicators...")
    tech = TechnicalIndicators(data)
    data_with_indicators = tech.add_all_indicators()
    print("✓ Calculated 20+ technical indicators\n")
    
    # Show indicators
    indicator_summary = tech.get_indicator_summary()
    print("Technical Indicators Summary:")
    print("-" * 60)
    
    for category, indicators in indicator_summary.items():
        print(f"\n{category.upper()}:")
        for name, value in indicators.items():
            if value is not None:
                print(f"  {name:15s}: {value:10.2f}")
    
    # Generate signals
    print("\n\nGenerating trading signals...")
    signal_gen = SignalGenerator(data_with_indicators)
    signals = signal_gen.generate_all_signals()
    print(f"✓ Generated {len(signals)} trading signals\n")
    
    # Show recommendation
    recommendation = signal_gen.get_current_recommendation()
    print("Trading Recommendation:")
    print("-" * 60)
    print(f"Recommendation: {recommendation['recommendation']}")
    print(f"Confidence:     {recommendation['confidence']:.1f}%")
    print(f"Buy Score:      {recommendation['buy_score']:.1f}")
    print(f"Sell Score:     {recommendation['sell_score']:.1f}")
    
    # Show recent signals
    print("\n\nRecent Trading Signals:")
    print("-" * 60)
    for signal in recommendation['recent_signals'][:5]:
        print(f"{signal['date'].strftime('%Y-%m-%d')}: {signal['type']:4s} - {signal['signal']:30s} ({signal['strength']})")
        print(f"  {signal['description']}")
    
    return data_with_indicators


def demo_portfolio():
    """
    Demonstrate portfolio tracking features
    """
    print("\n\n" + "="*70)
    print("DEMO: Portfolio Tracking")
    print("="*70 + "\n")
    
    from stock_ai_analyst import PortfolioTracker
    import os
    
    # Create demo portfolio
    portfolio_file = '/tmp/demo_portfolio.json'
    if os.path.exists(portfolio_file):
        os.remove(portfolio_file)
    
    tracker = PortfolioTracker(portfolio_file)
    
    # Add positions
    print("Building demo portfolio...\n")
    
    positions = [
        ('AAPL', 10, 150.00, 175.50),
        ('MSFT', 5, 300.00, 380.25),
        ('GOOGL', 3, 2800.00, 2950.00),
        ('TSLA', 8, 250.00, 245.75),
        ('NVDA', 15, 450.00, 875.00),
    ]
    
    for symbol, qty, buy_price, _ in positions:
        tracker.add_position(symbol, qty, buy_price)
        print(f"✓ Added {qty:2d} shares of {symbol} @ ${buy_price:.2f}")
    
    # Calculate current values
    current_prices = {symbol: current_price for symbol, _, _, current_price in positions}
    
    # Show portfolio summary
    print("\n\nPortfolio Summary:")
    print("-" * 60)
    
    summary = tracker.get_portfolio_summary(current_prices)
    
    for pos in summary['positions']:
        print(f"\n{pos['symbol']}:")
        print(f"  Quantity:       {pos['quantity']:8.0f} shares")
        print(f"  Avg Price:      ${pos['avg_price']:8.2f}")
        print(f"  Current Price:  ${pos['current_price']:8.2f}")
        print(f"  Cost Basis:     ${pos['cost_basis']:8.2f}")
        print(f"  Current Value:  ${pos['current_value']:8.2f}")
        print(f"  Profit/Loss:    ${pos['profit_loss']:8.2f} ({pos['profit_loss_pct']:+6.2f}%)")
    
    print("\n" + "="*60)
    print(f"Total Positions:    {summary['total_positions']}")
    print(f"Total Value:        ${summary['total_value']:,.2f}")
    print(f"Total Cost:         ${summary['total_cost']:,.2f}")
    print(f"Total Profit/Loss:  ${summary['total_profit_loss']:,.2f} ({summary['total_profit_loss_pct']:+.2f}%)")
    print("="*60)
    
    # Performance metrics
    metrics = tracker.get_performance_metrics(current_prices)
    
    print("\n\nPerformance Metrics:")
    print("-" * 60)
    print(f"Unrealized P/L:     ${metrics['unrealized_profit_loss']:,.2f} ({metrics['unrealized_profit_loss_pct']:+.2f}%)")
    print(f"Total Transactions: {metrics['total_transactions']}")
    
    if metrics['best_performer']:
        bp = metrics['best_performer']
        print(f"\nBest Performer:     {bp['symbol']} ({bp['profit_loss_pct']:+.2f}%)")
    
    if metrics['worst_performer']:
        wp = metrics['worst_performer']
        print(f"Worst Performer:    {wp['symbol']} ({wp['profit_loss_pct']:+.2f}%)")
    
    # Clean up
    if os.path.exists(portfolio_file):
        os.remove(portfolio_file)


def demo_visualization_info():
    """
    Show information about visualization features
    """
    print("\n\n" + "="*70)
    print("DEMO: Visualization Features")
    print("="*70 + "\n")
    
    print("The Stock AI Technical Analyst includes powerful visualization tools:\n")
    
    print("1. CANDLESTICK CHARTS")
    print("   - Traditional OHLC candlestick visualization")
    print("   - Volume bars")
    print("   - Interactive with mplfinance\n")
    
    print("2. TECHNICAL INDICATOR CHARTS")
    print("   - Moving Averages (SMA, EMA) overlay")
    print("   - Bollinger Bands")
    print("   - RSI subplot with overbought/oversold levels")
    print("   - MACD with histogram")
    print("   - Stochastic Oscillator")
    print("   - ADX (trend strength)\n")
    
    print("3. INTERACTIVE DASHBOARDS")
    print("   - Multi-panel layout with Plotly")
    print("   - Price & Volume")
    print("   - All major technical indicators")
    print("   - Exportable to HTML")
    print("   - Zoom, pan, and hover features\n")
    
    print("4. COMPARISON CHARTS")
    print("   - Compare multiple stocks")
    print("   - Normalized price changes")
    print("   - Side-by-side performance\n")
    
    print("Example usage:")
    print("-" * 60)
    print("from stock_ai_analyst import ChartVisualizer")
    print("")
    print("visualizer = ChartVisualizer(data_with_indicators, 'AAPL')")
    print("visualizer.create_dashboard('aapl_dashboard.html')")
    print("visualizer.plot_with_indicators('aapl_chart.html')")
    print("-" * 60)
    
    print("\n✓ Charts are saved as interactive HTML files")
    print("✓ Open in any web browser for full interactivity")


def demo_ai_features():
    """
    Show information about AI features
    """
    print("\n\n" + "="*70)
    print("DEMO: AI-Powered Assistant")
    print("="*70 + "\n")
    
    from stock_ai_analyst import AIAssistant
    
    assistant = AIAssistant()
    
    if assistant.has_ai:
        print("✓ AI features are ENABLED (OpenAI API key configured)\n")
    else:
        print("ℹ AI features require OpenAI API key\n")
        print("To enable AI features:")
        print("1. Get an API key from https://platform.openai.com/api-keys")
        print("2. Set environment variable: OPENAI_API_KEY=your_key")
        print("3. Or add to .env file\n")
    
    print("AI Assistant Capabilities:\n")
    
    print("1. COMPREHENSIVE STOCK ANALYSIS")
    print("   - Analyze stock data and technical indicators")
    print("   - Provide actionable insights")
    print("   - Clear buy/sell/hold recommendations\n")
    
    print("2. NATURAL LANGUAGE QUERIES")
    print("   - Ask questions in plain English")
    print("   - Get expert-level explanations")
    print("   - Context-aware responses\n")
    
    print("3. INDICATOR EXPLANATIONS")
    print("   - What indicators mean")
    print("   - How to interpret values")
    print("   - Trading strategies\n")
    
    print("4. PORTFOLIO ADVICE")
    print("   - Diversification suggestions")
    print("   - Risk management")
    print("   - Rebalancing recommendations\n")
    
    print("5. STOCK COMPARISONS")
    print("   - Compare multiple stocks")
    print("   - Ranking and scoring")
    print("   - Investment recommendations\n")
    
    print("Example usage:")
    print("-" * 60)
    print("assistant = AIAssistant()")
    print("")
    print("# Analyze a stock")
    print("analysis = assistant.analyze_stock(stock_data, indicators, signals)")
    print("")
    print("# Ask a question")
    print("response = assistant.query('What is RSI and how should I use it?')")
    print("")
    print("# Get portfolio advice")
    print("advice = assistant.portfolio_advice(portfolio_summary)")
    print("-" * 60)


def show_usage_examples():
    """
    Show practical usage examples
    """
    print("\n\n" + "="*70)
    print("USAGE EXAMPLES")
    print("="*70 + "\n")
    
    print("COMMAND LINE USAGE:\n")
    
    print("1. Analyze a stock:")
    print("   python main.py analyze --symbol AAPL --period 1y\n")
    
    print("2. Manage portfolio:")
    print("   python main.py portfolio\n")
    
    print("3. Chat with AI assistant:")
    print("   python main.py chat --symbol TSLA\n")
    
    print("\nPYTHON API USAGE:\n")
    
    print("Quick analysis example:")
    print("-" * 60)
    print("""
from stock_ai_analyst import StockAnalyzer, TechnicalIndicators, SignalGenerator

# Fetch and analyze
analyzer = StockAnalyzer('AAPL')
data = analyzer.fetch_data(period='1y')

# Calculate indicators
tech = TechnicalIndicators(data)
data_with_indicators = tech.add_all_indicators()

# Get trading signals
signals = SignalGenerator(data_with_indicators)
recommendation = signals.get_current_recommendation()

print(f"Recommendation: {recommendation['recommendation']}")
print(f"Confidence: {recommendation['confidence']:.1f}%")
""")
    print("-" * 60)


def main():
    """
    Run all demos
    """
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  Stock AI Technical Analyst - Interactive Demo".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    # Run demos
    data_with_indicators = demo_technical_analysis()
    demo_portfolio()
    demo_visualization_info()
    demo_ai_features()
    show_usage_examples()
    
    print("\n\n" + "="*70)
    print("Demo Complete!")
    print("="*70)
    print("\nNext Steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Try live analysis:    python main.py analyze --symbol AAPL")
    print("3. Run examples:         python examples.py")
    print("4. Read documentation:   README.md and QUICKSTART.md")
    print("\n" + "="*70 + "\n")


if __name__ == '__main__':
    main()
