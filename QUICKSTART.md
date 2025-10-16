# Quick Start Guide

## Getting Started in 5 Minutes

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/deepak160988/stock-ai-technical-analyst.git
cd stock-ai-technical-analyst

# Install dependencies
pip install -r requirements.txt
```

### 2. Basic Stock Analysis
```bash
# Analyze Apple stock
python main.py analyze --symbol AAPL
```

This will:
- ✅ Fetch 1 year of stock data
- ✅ Calculate 20+ technical indicators
- ✅ Generate buy/sell signals
- ✅ Create interactive charts (HTML files)
- ✅ Provide trading recommendation

### 3. View the Results

The command will generate two HTML files:
- `AAPL_dashboard.html` - Comprehensive technical analysis dashboard
- `AAPL_chart.html` - Interactive price chart with indicators

Open these files in your web browser to view the visualizations.

### 4. Try Portfolio Tracking
```bash
python main.py portfolio
```

Interactive menu to manage your portfolio:
1. View portfolio
2. Add position
3. Sell position
4. View transactions

### 5. AI Chat (Optional)

First, set up your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=your_key_here
```

Then chat with the AI assistant:
```bash
python main.py chat --symbol TSLA
```

## Quick Python Example

```python
from stock_ai_analyst import StockAnalyzer, TechnicalIndicators, SignalGenerator

# 1. Fetch data
analyzer = StockAnalyzer('AAPL')
data = analyzer.fetch_data(period='1y')

# 2. Calculate indicators
tech = TechnicalIndicators(data)
data_with_indicators = tech.add_all_indicators()

# 3. Generate signals
signals = SignalGenerator(data_with_indicators)
recommendation = signals.get_current_recommendation()

# 4. Print results
print(f"Recommendation: {recommendation['recommendation']}")
print(f"Confidence: {recommendation['confidence']:.1f}%")
```

## Common Use Cases

### Compare Multiple Stocks
```python
from stock_ai_analyst import StockAnalyzer

symbols = ['AAPL', 'MSFT', 'GOOGL']
for symbol in symbols:
    analyzer = StockAnalyzer(symbol)
    summary = analyzer.get_summary()
    print(f"{symbol}: ${summary['current_price']:.2f} ({summary['price_change_pct']:.2f}%)")
```

### Check if Stock is Oversold (RSI < 30)
```python
from stock_ai_analyst import StockAnalyzer, TechnicalIndicators

analyzer = StockAnalyzer('TSLA')
data = analyzer.fetch_data()
tech = TechnicalIndicators(data)
tech.add_rsi()

latest_rsi = tech.data['RSI'].iloc[-1]
if latest_rsi < 30:
    print("Stock is oversold - potential buy opportunity!")
```

### Track Portfolio Performance
```python
from stock_ai_analyst import PortfolioTracker, StockAnalyzer

tracker = PortfolioTracker()
tracker.add_position('AAPL', quantity=10, purchase_price=150.00)

# Get current price
analyzer = StockAnalyzer('AAPL')
current_price = analyzer.get_current_price()

# Calculate P/L
position = tracker.get_position_value('AAPL', current_price)
print(f"Profit/Loss: ${position['profit_loss']:.2f} ({position['profit_loss_pct']:.2f}%)")
```

## Next Steps

1. **Run examples**: `python examples.py`
2. **Read the docs**: Check `README.md` for full documentation
3. **Explore the code**: Look at the `stock_ai_analyst/` directory
4. **Try different stocks**: Experiment with various symbols
5. **Customize indicators**: Modify parameters in the code

## Tips

- 💡 Use longer periods (1y, 2y) for better trend analysis
- 💡 Combine multiple indicators for stronger signals
- 💡 Check multiple timeframes (daily, weekly, monthly)
- 💡 Always do your own research before trading
- 💡 Past performance doesn't guarantee future results

## Troubleshooting

**Problem**: "No data found for symbol"
- **Solution**: Check if the symbol is correct and available on Yahoo Finance

**Problem**: Charts not generating
- **Solution**: Ensure matplotlib and plotly are installed correctly

**Problem**: AI features not working
- **Solution**: Set OPENAI_API_KEY in .env file

**Problem**: Import errors
- **Solution**: Run `pip install -r requirements.txt` again

## Support

For help:
- Check the examples: `python examples.py`
- Read README.md
- Open an issue on GitHub
