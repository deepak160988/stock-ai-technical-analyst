#!/usr/bin/env python3
"""
Basic tests for Stock AI Technical Analyst
"""
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from stock_ai_analyst import (
            StockAnalyzer,
            TechnicalIndicators,
            ChartVisualizer,
            SignalGenerator,
            PortfolioTracker,
            AIAssistant
        )
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_stock_analyzer():
    """Test StockAnalyzer basic functionality"""
    print("\nTesting StockAnalyzer...")
    
    try:
        from stock_ai_analyst import StockAnalyzer
        
        # Create analyzer
        analyzer = StockAnalyzer('AAPL')
        print(f"✓ Created analyzer for AAPL")
        
        # Fetch data (small period for speed)
        data = analyzer.fetch_data(period='5d', interval='1d')
        if not data.empty:
            print(f"✓ Fetched {len(data)} days of data")
        else:
            print("✗ No data fetched")
            return False
        
        # Get summary
        summary = analyzer.get_summary()
        if 'symbol' in summary and 'current_price' in summary:
            print(f"✓ Got summary: {summary['symbol']} @ ${summary['current_price']:.2f}")
        else:
            print("✗ Summary incomplete")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_technical_indicators():
    """Test TechnicalIndicators"""
    print("\nTesting TechnicalIndicators...")
    
    try:
        from stock_ai_analyst import StockAnalyzer, TechnicalIndicators
        
        # Get data
        analyzer = StockAnalyzer('MSFT')
        data = analyzer.fetch_data(period='3mo', interval='1d')
        
        # Calculate indicators
        tech = TechnicalIndicators(data)
        data_with_indicators = tech.add_all_indicators()
        
        # Check if indicators were added
        required_indicators = ['RSI', 'MACD', 'SMA_20', 'BB_High']
        missing = [ind for ind in required_indicators if ind not in data_with_indicators.columns]
        
        if not missing:
            print(f"✓ All technical indicators calculated")
            
            # Get latest values
            latest = tech.get_latest_values()
            print(f"  RSI: {latest.get('RSI', 0):.2f}")
            print(f"  MACD: {latest.get('MACD', 0):.2f}")
            return True
        else:
            print(f"✗ Missing indicators: {missing}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_signals():
    """Test SignalGenerator"""
    print("\nTesting SignalGenerator...")
    
    try:
        from stock_ai_analyst import StockAnalyzer, TechnicalIndicators, SignalGenerator
        
        # Get data with indicators
        analyzer = StockAnalyzer('GOOGL')
        data = analyzer.fetch_data(period='6mo')
        
        tech = TechnicalIndicators(data)
        data_with_indicators = tech.add_all_indicators()
        
        # Generate signals
        signal_gen = SignalGenerator(data_with_indicators)
        signals = signal_gen.generate_all_signals()
        
        print(f"✓ Generated {len(signals)} signals")
        
        # Get recommendation
        recommendation = signal_gen.get_current_recommendation()
        if 'recommendation' in recommendation:
            print(f"✓ Recommendation: {recommendation['recommendation']}")
            return True
        else:
            print("✗ No recommendation generated")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_portfolio():
    """Test PortfolioTracker"""
    print("\nTesting PortfolioTracker...")
    
    try:
        from stock_ai_analyst import PortfolioTracker
        import os
        
        # Use a test file
        test_file = '/tmp/test_portfolio.json'
        if os.path.exists(test_file):
            os.remove(test_file)
        
        # Create tracker
        tracker = PortfolioTracker(test_file)
        
        # Add position
        tracker.add_position('AAPL', 10, 150.00)
        print("✓ Added position")
        
        # Check position
        positions = tracker.get_positions()
        if 'AAPL' in positions:
            print("✓ Position saved")
        else:
            print("✗ Position not saved")
            return False
        
        # Get value
        position_value = tracker.get_position_value('AAPL', 175.00)
        if 'profit_loss' in position_value:
            print(f"✓ Calculated P/L: ${position_value['profit_loss']:.2f}")
        else:
            print("✗ Could not calculate P/L")
            return False
        
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)
        
        return True
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_ai_assistant():
    """Test AIAssistant (without API key)"""
    print("\nTesting AIAssistant...")
    
    try:
        from stock_ai_analyst import AIAssistant
        
        # Create assistant (will not have API key in test environment)
        assistant = AIAssistant()
        print("✓ Created AIAssistant")
        
        if assistant.has_ai:
            print("✓ AI features available (API key configured)")
        else:
            print("ℹ AI features not available (no API key, this is expected)")
        
        return True
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_visualization():
    """Test ChartVisualizer"""
    print("\nTesting ChartVisualizer...")
    
    try:
        from stock_ai_analyst import StockAnalyzer, TechnicalIndicators, ChartVisualizer
        
        # Get data with indicators
        analyzer = StockAnalyzer('TSLA')
        data = analyzer.fetch_data(period='1mo')
        
        tech = TechnicalIndicators(data)
        data_with_indicators = tech.add_all_indicators()
        
        # Create visualizer
        visualizer = ChartVisualizer(data_with_indicators, 'TSLA')
        print("✓ Created ChartVisualizer")
        
        return True
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("Stock AI Technical Analyst - Test Suite")
    print("="*60)
    
    tests = [
        test_imports,
        test_stock_analyzer,
        test_technical_indicators,
        test_signals,
        test_portfolio,
        test_ai_assistant,
        test_visualization,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    print("\n" + "="*60)
    print("Test Results")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
