#!/usr/bin/env python3
"""
Main application for Stock AI Technical Analyst
"""
import argparse
import sys
from stock_ai_analyst import (
    StockAnalyzer,
    TechnicalIndicators,
    ChartVisualizer,
    SignalGenerator,
    PortfolioTracker,
    AIAssistant
)
from dotenv import load_dotenv


def analyze_stock(symbol: str, period: str = "1y", generate_charts: bool = True):
    """
    Perform comprehensive stock analysis
    
    Args:
        symbol: Stock symbol
        period: Time period for analysis
        generate_charts: Whether to generate visualization charts
    """
    print(f"\n{'='*60}")
    print(f"Stock Analysis for {symbol}")
    print(f"{'='*60}\n")
    
    # Initialize analyzer
    analyzer = StockAnalyzer(symbol)
    
    # Fetch data
    print("Fetching stock data...")
    data = analyzer.fetch_data(period=period)
    
    if data.empty:
        print(f"Error: No data found for {symbol}")
        return
    
    # Get summary
    summary = analyzer.get_summary()
    print("\n--- Stock Summary ---")
    for key, value in summary.items():
        print(f"{key}: {value}")
    
    # Calculate technical indicators
    print("\n\nCalculating technical indicators...")
    tech_indicators = TechnicalIndicators(data)
    data_with_indicators = tech_indicators.add_all_indicators()
    
    indicator_summary = tech_indicators.get_indicator_summary()
    print("\n--- Technical Indicators ---")
    for category, indicators in indicator_summary.items():
        print(f"\n{category.upper()}:")
        for name, value in indicators.items():
            if value is not None:
                print(f"  {name}: {value:.2f}")
    
    # Generate signals
    print("\n\nGenerating trading signals...")
    signal_gen = SignalGenerator(data_with_indicators)
    signals = signal_gen.generate_all_signals()
    
    recommendation = signal_gen.get_current_recommendation()
    print("\n--- Trading Recommendation ---")
    print(f"Recommendation: {recommendation['recommendation']}")
    print(f"Confidence: {recommendation['confidence']:.1f}%")
    print(f"Buy Score: {recommendation['buy_score']:.1f}")
    print(f"Sell Score: {recommendation['sell_score']:.1f}")
    
    print("\n--- Recent Signals ---")
    for signal in recommendation['recent_signals']:
        print(f"{signal['date'].strftime('%Y-%m-%d')}: {signal['type']} - {signal['signal']} ({signal['strength']})")
        print(f"  {signal['description']}")
    
    # Generate visualizations
    if generate_charts:
        print("\n\nGenerating charts...")
        visualizer = ChartVisualizer(data_with_indicators, symbol)
        
        try:
            # Create dashboard
            dashboard_file = f"{symbol}_dashboard.html"
            visualizer.create_dashboard(output_file=dashboard_file)
            print(f"Dashboard saved to: {dashboard_file}")
            
            # Create interactive chart
            chart_file = f"{symbol}_chart.html"
            visualizer.plot_with_indicators(output_file=chart_file)
            print(f"Interactive chart saved to: {chart_file}")
        except Exception as e:
            print(f"Error generating charts: {e}")
    
    print(f"\n{'='*60}\n")


def manage_portfolio():
    """
    Interactive portfolio management
    """
    print("\n--- Portfolio Manager ---\n")
    
    tracker = PortfolioTracker()
    
    while True:
        print("\nOptions:")
        print("1. View portfolio")
        print("2. Add position")
        print("3. Sell position")
        print("4. View transactions")
        print("5. Exit")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            positions = tracker.get_positions()
            if not positions:
                print("\nNo positions in portfolio.")
            else:
                print("\n--- Current Positions ---")
                current_prices = {}
                for symbol in positions:
                    try:
                        analyzer = StockAnalyzer(symbol)
                        current_prices[symbol] = analyzer.get_current_price()
                    except:
                        current_prices[symbol] = 0
                
                summary = tracker.get_portfolio_summary(current_prices)
                
                for pos in summary['positions']:
                    print(f"\n{pos['symbol']}:")
                    print(f"  Quantity: {pos['quantity']}")
                    print(f"  Avg Price: ${pos['avg_price']:.2f}")
                    print(f"  Current Price: ${pos['current_price']:.2f}")
                    print(f"  P/L: ${pos['profit_loss']:.2f} ({pos['profit_loss_pct']:.2f}%)")
                
                print(f"\n--- Portfolio Summary ---")
                print(f"Total Value: ${summary['total_value']:.2f}")
                print(f"Total Cost: ${summary['total_cost']:.2f}")
                print(f"Total P/L: ${summary['total_profit_loss']:.2f} ({summary['total_profit_loss_pct']:.2f}%)")
        
        elif choice == '2':
            symbol = input("Enter stock symbol: ").strip().upper()
            try:
                quantity = float(input("Enter quantity: "))
                price = float(input("Enter purchase price: "))
                tracker.add_position(symbol, quantity, price)
                print(f"\nAdded {quantity} shares of {symbol} at ${price:.2f}")
            except ValueError:
                print("Invalid input. Please enter valid numbers.")
        
        elif choice == '3':
            symbol = input("Enter stock symbol: ").strip().upper()
            try:
                quantity = float(input("Enter quantity to sell: "))
                price = float(input("Enter sale price: "))
                result = tracker.remove_position(symbol, quantity, price)
                print(f"\nSold {quantity} shares of {symbol} at ${price:.2f}")
                print(f"P/L: ${result['profit_loss']:.2f} ({result['profit_loss_pct']:.2f}%)")
            except (ValueError, Exception) as e:
                print(f"Error: {e}")
        
        elif choice == '4':
            transactions = tracker.get_transaction_history()
            if not transactions:
                print("\nNo transactions found.")
            else:
                print("\n--- Transaction History ---")
                for t in transactions[:10]:  # Show last 10
                    print(f"{t['date'][:10]}: {t['type']} {t['quantity']} {t['symbol']} @ ${t['price']:.2f}")
                    if 'profit_loss' in t:
                        print(f"  P/L: ${t['profit_loss']:.2f}")
        
        elif choice == '5':
            break
        else:
            print("Invalid option.")


def ai_chat(symbol: str = None):
    """
    Interactive AI chat assistant
    
    Args:
        symbol: Optional stock symbol to analyze
    """
    print("\n--- AI Stock Assistant ---")
    print("Ask me anything about stocks and technical analysis!")
    print("Type 'exit' to quit.\n")
    
    assistant = AIAssistant()
    
    if not assistant.has_ai:
        print("⚠️  AI features require OpenAI API key.")
        print("Set OPENAI_API_KEY environment variable to enable AI chat.\n")
        return
    
    # If symbol provided, load context
    context = None
    if symbol:
        try:
            analyzer = StockAnalyzer(symbol)
            data = analyzer.fetch_data()
            summary = analyzer.get_summary()
            
            tech_indicators = TechnicalIndicators(data)
            tech_indicators.add_all_indicators()
            indicator_summary = tech_indicators.get_indicator_summary()
            
            signal_gen = SignalGenerator(tech_indicators.data)
            recommendation = signal_gen.get_current_recommendation()
            
            context = {
                'stock_data': summary,
                'indicators': indicator_summary,
                'signals': recommendation
            }
            
            # Get initial analysis
            print(f"Analyzing {symbol}...\n")
            analysis = assistant.analyze_stock(summary, indicator_summary, recommendation)
            print(analysis)
            print("\n" + "="*60 + "\n")
        except Exception as e:
            print(f"Error loading stock data: {e}\n")
    
    while True:
        question = input("You: ").strip()
        
        if question.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye!")
            break
        
        if not question:
            continue
        
        response = assistant.query(question, context)
        print(f"\nAssistant: {response}\n")


def main():
    """
    Main entry point
    """
    load_dotenv()
    
    parser = argparse.ArgumentParser(
        description='Stock AI Technical Analyst - Comprehensive stock analysis tool'
    )
    
    parser.add_argument(
        'command',
        choices=['analyze', 'portfolio', 'chat'],
        help='Command to run'
    )
    
    parser.add_argument(
        '--symbol', '-s',
        type=str,
        help='Stock symbol (required for analyze and chat)'
    )
    
    parser.add_argument(
        '--period', '-p',
        type=str,
        default='1y',
        help='Time period for analysis (default: 1y)'
    )
    
    parser.add_argument(
        '--no-charts',
        action='store_true',
        help='Skip chart generation'
    )
    
    args = parser.parse_args()
    
    if args.command == 'analyze':
        if not args.symbol:
            print("Error: --symbol is required for analyze command")
            sys.exit(1)
        analyze_stock(args.symbol, args.period, not args.no_charts)
    
    elif args.command == 'portfolio':
        manage_portfolio()
    
    elif args.command == 'chat':
        ai_chat(args.symbol)


if __name__ == '__main__':
    main()
