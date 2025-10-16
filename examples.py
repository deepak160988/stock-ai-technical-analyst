#!/usr/bin/env python3
"""
Example usage of Stock AI Technical Analyst
"""
from stock_ai_analyst import (
    StockAnalyzer,
    TechnicalIndicators,
    ChartVisualizer,
    SignalGenerator,
    PortfolioTracker,
    AIAssistant
)


def example_basic_analysis():
    """
    Example: Basic stock analysis
    """
    print("\n=== Example 1: Basic Stock Analysis ===\n")
    
    # Initialize analyzer for Apple stock
    analyzer = StockAnalyzer('AAPL')
    
    # Fetch 1 year of data
    data = analyzer.fetch_data(period='1y')
    print(f"Fetched {len(data)} days of data")
    
    # Get stock summary
    summary = analyzer.get_summary()
    print(f"\nCurrent Price: ${summary['current_price']:.2f}")
    print(f"52-Week High: ${summary['high_52w']:.2f}")
    print(f"52-Week Low: ${summary['low_52w']:.2f}")
    print(f"Price Change: {summary['price_change_pct']:.2f}%")


def example_technical_indicators():
    """
    Example: Calculate technical indicators
    """
    print("\n=== Example 2: Technical Indicators ===\n")
    
    # Fetch data
    analyzer = StockAnalyzer('MSFT')
    data = analyzer.fetch_data(period='6mo')
    
    # Calculate indicators
    tech_indicators = TechnicalIndicators(data)
    data_with_indicators = tech_indicators.add_all_indicators()
    
    # Get latest values
    latest = tech_indicators.get_latest_values()
    
    print("Latest Technical Indicators for MSFT:")
    print(f"RSI: {latest.get('RSI', 0):.2f}")
    print(f"MACD: {latest.get('MACD', 0):.2f}")
    print(f"SMA 20: ${latest.get('SMA_20', 0):.2f}")
    print(f"SMA 50: ${latest.get('SMA_50', 0):.2f}")
    
    # Get indicator summary
    summary = tech_indicators.get_indicator_summary()
    print("\nIndicator Summary:")
    for category, indicators in summary.items():
        print(f"\n{category.upper()}:")
        for name, value in indicators.items():
            if value is not None:
                print(f"  {name}: {value:.2f}")


def example_signals():
    """
    Example: Generate trading signals
    """
    print("\n=== Example 3: Trading Signals ===\n")
    
    # Fetch and analyze
    analyzer = StockAnalyzer('GOOGL')
    data = analyzer.fetch_data(period='1y')
    
    tech_indicators = TechnicalIndicators(data)
    data_with_indicators = tech_indicators.add_all_indicators()
    
    # Generate signals
    signal_gen = SignalGenerator(data_with_indicators)
    signals = signal_gen.generate_all_signals()
    
    print(f"Generated {len(signals)} signals")
    
    # Get recommendation
    recommendation = signal_gen.get_current_recommendation()
    
    print(f"\nRecommendation: {recommendation['recommendation']}")
    print(f"Confidence: {recommendation['confidence']:.1f}%")
    print(f"Buy Score: {recommendation['buy_score']:.1f}")
    print(f"Sell Score: {recommendation['sell_score']:.1f}")
    
    print("\nRecent Signals:")
    for signal in recommendation['recent_signals'][:3]:
        print(f"  {signal['date'].strftime('%Y-%m-%d')}: {signal['type']} - {signal['signal']}")


def example_visualization():
    """
    Example: Create visualizations
    """
    print("\n=== Example 4: Visualization ===\n")
    
    # Fetch and analyze
    analyzer = StockAnalyzer('TSLA')
    data = analyzer.fetch_data(period='3mo')
    
    tech_indicators = TechnicalIndicators(data)
    data_with_indicators = tech_indicators.add_all_indicators()
    
    # Create visualizer
    visualizer = ChartVisualizer(data_with_indicators, 'TSLA')
    
    # Generate interactive chart
    print("Generating interactive chart...")
    visualizer.plot_with_indicators(output_file='tesla_analysis.html')
    print("Chart saved to: tesla_analysis.html")
    
    # Generate dashboard
    print("Generating dashboard...")
    visualizer.create_dashboard(output_file='tesla_dashboard.html')
    print("Dashboard saved to: tesla_dashboard.html")


def example_portfolio():
    """
    Example: Portfolio tracking
    """
    print("\n=== Example 5: Portfolio Tracking ===\n")
    
    # Create portfolio tracker
    tracker = PortfolioTracker('example_portfolio.json')
    
    # Add positions
    print("Adding positions...")
    tracker.add_position('AAPL', 10, 150.00)
    tracker.add_position('MSFT', 5, 300.00)
    tracker.add_position('GOOGL', 3, 2800.00)
    
    # Get current prices
    current_prices = {}
    for symbol in ['AAPL', 'MSFT', 'GOOGL']:
        analyzer = StockAnalyzer(symbol)
        current_prices[symbol] = analyzer.get_current_price()
    
    # Get portfolio summary
    summary = tracker.get_portfolio_summary(current_prices)
    
    print(f"\nPortfolio Summary:")
    print(f"Total Positions: {summary['total_positions']}")
    print(f"Total Value: ${summary['total_value']:.2f}")
    print(f"Total Cost: ${summary['total_cost']:.2f}")
    print(f"Total P/L: ${summary['total_profit_loss']:.2f} ({summary['total_profit_loss_pct']:.2f}%)")
    
    print("\nPositions:")
    for pos in summary['positions']:
        print(f"  {pos['symbol']}: {pos['quantity']} shares @ ${pos['avg_price']:.2f}")
        print(f"    Current: ${pos['current_price']:.2f}, P/L: ${pos['profit_loss']:.2f} ({pos['profit_loss_pct']:.2f}%)")


def example_ai_assistant():
    """
    Example: AI Assistant
    """
    print("\n=== Example 6: AI Assistant ===\n")
    
    # Create AI assistant
    assistant = AIAssistant()
    
    if not assistant.has_ai:
        print("⚠️  AI features require OpenAI API key.")
        print("Set OPENAI_API_KEY environment variable to enable AI features.")
        return
    
    # Get stock data
    analyzer = StockAnalyzer('NVDA')
    data = analyzer.fetch_data(period='6mo')
    summary = analyzer.get_summary()
    
    tech_indicators = TechnicalIndicators(data)
    tech_indicators.add_all_indicators()
    indicator_summary = tech_indicators.get_indicator_summary()
    
    signal_gen = SignalGenerator(tech_indicators.data)
    recommendation = signal_gen.get_current_recommendation()
    
    # Get AI analysis
    print("Getting AI analysis for NVDA...\n")
    analysis = assistant.analyze_stock(summary, indicator_summary, recommendation)
    print(analysis)
    
    # Ask a question
    print("\n" + "="*60 + "\n")
    question = "What does the RSI indicator tell us about NVDA's momentum?"
    print(f"Question: {question}\n")
    response = assistant.query(question, {'indicators': indicator_summary})
    print(f"Answer: {response}")


def run_all_examples():
    """
    Run all examples
    """
    examples = [
        example_basic_analysis,
        example_technical_indicators,
        example_signals,
        example_visualization,
        example_portfolio,
        example_ai_assistant,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\nError in {example.__name__}: {e}")
        
        print("\n" + "="*80 + "\n")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        example_name = sys.argv[1]
        example_func = globals().get(f'example_{example_name}')
        if example_func:
            example_func()
        else:
            print(f"Unknown example: {example_name}")
            print("Available examples: basic_analysis, technical_indicators, signals, visualization, portfolio, ai_assistant")
    else:
        run_all_examples()
