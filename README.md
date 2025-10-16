# Stock AI Technical Analyst 📈🤖

A comprehensive AI-powered stock technical analysis assistant that provides real-time analysis, technical indicators, visualization, buy/sell signals, portfolio tracking, and natural language queries.

## Features ✨

### 📊 Real-Time Stock Analysis
- Fetch real-time and historical stock data using Yahoo Finance
- Get comprehensive stock summaries including price, volume, market cap, and more
- Support for multiple time periods and intervals

### 📐 Technical Indicators
Calculate and analyze 20+ technical indicators:
- **Trend Indicators**: SMA, EMA, ADX
- **Momentum Indicators**: RSI, MACD, Stochastic Oscillator
- **Volatility Indicators**: Bollinger Bands, ATR
- **Volume Indicators**: OBV (On-Balance Volume)

### 📈 Advanced Visualization
- Interactive candlestick charts with Plotly
- Multi-indicator dashboards
- Stock comparison charts
- Technical analysis overlays (moving averages, Bollinger Bands, etc.)
- Exportable HTML charts

### 🎯 Buy/Sell Signals
Automated signal generation based on:
- Moving average crossovers (Golden Cross, Death Cross)
- RSI oversold/overbought conditions
- MACD crossovers
- Bollinger Band bounces
- Stochastic oscillator patterns
- Trend strength analysis

### 💼 Portfolio Tracking
- Track multiple stock positions
- Calculate unrealized and realized gains/losses
- Portfolio performance metrics
- Transaction history
- Win rate analysis
- Best/worst performer identification

### 🤖 AI-Powered Assistant
- Natural language queries about stocks
- Comprehensive stock analysis with AI insights
- Technical indicator explanations
- Portfolio advice
- Stock comparisons
- Powered by OpenAI GPT models

## Installation 🚀

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/deepak160988/stock-ai-technical-analyst.git
cd stock-ai-technical-analyst
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up environment variables for AI features:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

4. Install the package:
```bash
pip install -e .
```

## Usage 📖

### Command Line Interface

#### 1. Analyze a Stock
```bash
python main.py analyze --symbol AAPL --period 1y
```

Options:
- `--symbol` or `-s`: Stock symbol (required)
- `--period` or `-p`: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)
- `--no-charts`: Skip chart generation

#### 2. Portfolio Management
```bash
python main.py portfolio
```

Interactive menu to:
- View current positions
- Add new positions
- Sell positions
- View transaction history

#### 3. AI Chat Assistant
```bash
python main.py chat --symbol TSLA
```

Chat with the AI assistant about stocks and technical analysis.

### Python API

#### Basic Analysis
```python
from stock_ai_analyst import StockAnalyzer

# Initialize analyzer
analyzer = StockAnalyzer('AAPL')

# Fetch data
data = analyzer.fetch_data(period='1y')

# Get summary
summary = analyzer.get_summary()
print(f"Current Price: ${summary['current_price']:.2f}")
```

#### Technical Indicators
```python
from stock_ai_analyst import TechnicalIndicators

# Calculate indicators
tech_indicators = TechnicalIndicators(data)
data_with_indicators = tech_indicators.add_all_indicators()

# Get latest values
latest = tech_indicators.get_latest_values()
print(f"RSI: {latest['RSI']:.2f}")
print(f"MACD: {latest['MACD']:.2f}")
```

#### Generate Signals
```python
from stock_ai_analyst import SignalGenerator

# Generate signals
signal_gen = SignalGenerator(data_with_indicators)
recommendation = signal_gen.get_current_recommendation()

print(f"Recommendation: {recommendation['recommendation']}")
print(f"Confidence: {recommendation['confidence']:.1f}%")
```

#### Create Visualizations
```python
from stock_ai_analyst import ChartVisualizer

# Create visualizer
visualizer = ChartVisualizer(data_with_indicators, 'AAPL')

# Generate dashboard
visualizer.create_dashboard(output_file='dashboard.html')

# Generate interactive chart
visualizer.plot_with_indicators(output_file='chart.html')
```

#### Portfolio Tracking
```python
from stock_ai_analyst import PortfolioTracker

# Create tracker
tracker = PortfolioTracker()

# Add position
tracker.add_position('AAPL', quantity=10, purchase_price=150.00)

# Get portfolio summary
current_prices = {'AAPL': 175.00}
summary = tracker.get_portfolio_summary(current_prices)
print(f"Total P/L: ${summary['total_profit_loss']:.2f}")
```

#### AI Assistant
```python
from stock_ai_analyst import AIAssistant

# Create assistant (requires OPENAI_API_KEY)
assistant = AIAssistant()

# Get stock analysis
analysis = assistant.analyze_stock(stock_data, indicators, signals)
print(analysis)

# Ask a question
response = assistant.query("What is RSI and how do I use it?")
print(response)
```

## Examples 💡

Run the examples script to see all features in action:

```bash
python examples.py
```

Or run specific examples:
```bash
python examples.py basic_analysis
python examples.py technical_indicators
python examples.py signals
python examples.py visualization
python examples.py portfolio
python examples.py ai_assistant
```

## Technical Indicators Explained 📚

### RSI (Relative Strength Index)
- **Range**: 0-100
- **Overbought**: > 70
- **Oversold**: < 30
- **Use**: Identify potential reversal points

### MACD (Moving Average Convergence Divergence)
- **Signals**: Crossovers between MACD line and signal line
- **Bullish**: MACD crosses above signal
- **Bearish**: MACD crosses below signal

### Bollinger Bands
- **Components**: Upper band, middle band (SMA), lower band
- **Volatility**: Band width indicates volatility
- **Signals**: Price touching bands can indicate overbought/oversold

### Stochastic Oscillator
- **Range**: 0-100
- **Overbought**: > 80
- **Oversold**: < 20
- **Use**: Momentum indicator for timing entries/exits

### ADX (Average Directional Index)
- **Range**: 0-100
- **Strong Trend**: > 25
- **Weak Trend**: < 20
- **Use**: Measure trend strength

## Architecture 🏗️

```
stock-ai-technical-analyst/
├── stock_ai_analyst/          # Main package
│   ├── __init__.py           # Package initialization
│   ├── stock_analyzer.py     # Stock data fetching
│   ├── technical_indicators.py  # Technical indicators
│   ├── visualization.py      # Chart generation
│   ├── signals.py            # Signal generation
│   ├── portfolio.py          # Portfolio tracking
│   └── ai_assistant.py       # AI chat interface
├── main.py                   # CLI entry point
├── examples.py               # Usage examples
├── requirements.txt          # Dependencies
├── setup.py                  # Package setup
├── .env.example             # Environment template
└── README.md                # Documentation
```

## Dependencies 📦

Core libraries:
- **yfinance**: Stock data fetching
- **pandas**: Data manipulation
- **numpy**: Numerical computations
- **ta**: Technical analysis library
- **matplotlib/plotly**: Visualization
- **langchain**: AI integration
- **openai**: GPT models

## Configuration ⚙️

### Environment Variables

Create a `.env` file:
```
OPENAI_API_KEY=your_api_key_here
PORTFOLIO_FILE=portfolio.json
```

### API Keys

To use AI features, get an OpenAI API key:
1. Visit https://platform.openai.com/api-keys
2. Create an account
3. Generate an API key
4. Add to `.env` file

## Limitations & Disclaimers ⚠️

- **Not Financial Advice**: This tool is for educational and informational purposes only
- **Data Accuracy**: Relies on Yahoo Finance data availability
- **AI Limitations**: AI responses should be verified with your own research
- **Past Performance**: Historical data does not guarantee future results
- **Do Your Own Research**: Always consult with a financial advisor before making investment decisions

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License.

## Support 💬

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review examples

## Roadmap 🗺️

Future enhancements:
- [ ] Real-time streaming data
- [ ] More technical indicators (Ichimoku, Fibonacci, etc.)
- [ ] Backtesting engine
- [ ] Multi-timeframe analysis
- [ ] Sentiment analysis from news
- [ ] API server mode
- [ ] Web dashboard
- [ ] Mobile app

## Acknowledgments 🙏

Built with:
- Yahoo Finance API
- OpenAI GPT
- Python data science ecosystem

---

**Disclaimer**: This software is provided "as is" without warranty. Use at your own risk. Not financial advice.
