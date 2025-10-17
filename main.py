from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from config.settings import settings
    logger.info("✓ Settings imported")
except Exception as e:
    logger.warning(f"Settings import failed: {e}")
    class MockSettings:
        API_TITLE = "Stock AI Technical Analyst API"
        API_VERSION = "1.0.0"
    settings = MockSettings()

try:
    from services.stock_service import StockService
    stock_service = StockService()
    logger.info("✓ Stock service imported")
except Exception as e:
    logger.warning(f"Stock service import failed: {e}")
    stock_service = None

try:
    from services.indicators_service import IndicatorsService
    indicators_service = IndicatorsService()
    logger.info("✓ Indicators service imported")
except Exception as e:
    logger.warning(f"Indicators service import failed: {e}")
    indicators_service = None

try:
    from services.signals_service import SignalsService
    signals_service = SignalsService()
    logger.info("✓ Signals service imported")
except Exception as e:
    logger.warning(f"Signals service import failed: {e}")
    signals_service = None

try:
    from services.portfolio_service import PortfolioService
    portfolio_service = PortfolioService()
    logger.info("✓ Portfolio service imported")
except Exception as e:
    logger.warning(f"Portfolio service import failed: {e}")
    portfolio_service = None

try:
    from services.ai_service import AIService
    ai_service = AIService()
    logger.info("✓ AI service imported")
except Exception as e:
    logger.warning(f"AI service import failed: {e}")
    ai_service = None

try:
    from services.indian_stock_service import IndianStockService
    indian_stock_service = IndianStockService()
    logger.info("✓ Indian stock service imported")
except Exception as e:
    logger.warning(f"Indian stock service import failed: {e}")
    indian_stock_service = None

app = FastAPI(title="Stock AI Technical Analyst API", version="1.0.0", docs_url="/docs", redoc_url="/redoc")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
async def root():
    return {"message": "Welcome to Stock AI Technical Analyst API", "version": "1.0.0", "documentation": "/docs", "status": "active", "timestamp": datetime.now().isoformat()}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Stock AI Technical Analyst API", "version": "1.0.0", "timestamp": datetime.now().isoformat()}

@app.get("/api/stocks/{symbol}")
async def get_stock_data(symbol: str, days: int = Query(365, ge=1, le=1000)):
    try:
        if not stock_service:
            raise HTTPException(status_code=503, detail="Stock service not available")
        if not stock_service.validate_symbol(symbol.upper()):
            raise HTTPException(status_code=404, detail=f"Symbol {symbol} not found")
        df = stock_service.get_historical_data(symbol.upper(), days)
        if df.empty:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")
        latest_price = df['Close'].iloc[-1]
        prices = [{"date": idx.isoformat(), "open": float(row['Open']), "high": float(row['High']), "low": float(row['Low']), "close": float(row['Close']), "volume": int(row['Volume'])} for idx, row in df.iterrows()]
        logger.info(f"Retrieved {len(prices)} days of data for {symbol}")
        return {"symbol": symbol.upper(), "prices": prices, "current_price": float(latest_price), "currency": "USD", "last_updated": datetime.now().isoformat(), "data_points": len(prices)}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/stocks/{symbol}/latest")
async def get_latest_price(symbol: str):
    try:
        if not stock_service:
            raise HTTPException(status_code=503, detail="Stock service not available")
        latest_price = stock_service.get_latest_price(symbol.upper())
        if latest_price is None:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")
        stock_info = stock_service.get_stock_info(symbol.upper())
        logger.info(f"Retrieved latest price for {symbol}: ${latest_price}")
        return {"symbol": symbol.upper(), "price": latest_price, "currency": "USD", "name": stock_info.get("name"), "sector": stock_info.get("sector"), "timestamp": datetime.now().isoformat()}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/indicators/{symbol}")
async def get_indicators(symbol: str, days: int = Query(365, ge=1, le=1000)):
    try:
        if not stock_service or not indicators_service:
            raise HTTPException(status_code=503, detail="Services not available")
        df = stock_service.get_historical_data(symbol.upper(), days)
        if df.empty:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")
        indicators = indicators_service.get_all_indicators(df)
        if not indicators:
            raise HTTPException(status_code=500, detail="Error calculating indicators")
        logger.info(f"Calculated indicators for {symbol}")
        return {"symbol": symbol.upper(), "indicators": indicators, "data_points": len(df), "timestamp": datetime.now().isoformat()}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/indicators/{symbol}/rsi")
async def get_rsi(symbol: str, days: int = Query(365, ge=1, le=1000), window: int = Query(14, ge=5, le=100)):
    try:
        if not stock_service or not indicators_service:
            raise HTTPException(status_code=503, detail="Services not available")
        df = stock_service.get_historical_data(symbol.upper(), days)
        if df.empty:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")
        prices = df['Close'].tolist()
        rsi, overbought, oversold = indicators_service.calculate_rsi(prices, window)
        logger.info(f"Calculated RSI for {symbol}")
        return {"symbol": symbol.upper(), "indicator": "rsi", "window": window, "values": rsi, "overbought_flags": overbought, "oversold_flags": oversold, "data_points": len(rsi), "latest_rsi": rsi[-1] if rsi else None, "timestamp": datetime.now().isoformat()}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/indicators/{symbol}/macd")
async def get_macd(symbol: str, days: int = Query(365, ge=1, le=1000)):
    try:
        if not stock_service or not indicators_service:
            raise HTTPException(status_code=503, detail="Services not available")
        df = stock_service.get_historical_data(symbol.upper(), days)
        if df.empty:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")
        prices = df['Close'].tolist()
        macd_line, signal_line, histogram = indicators_service.calculate_macd(prices)
        logger.info(f"Calculated MACD for {symbol}")
        return {"symbol": symbol.upper(), "indicator": "macd", "macd_line": macd_line, "signal_line": signal_line, "histogram": histogram, "data_points": len(macd_line), "timestamp": datetime.now().isoformat()}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/indicators/{symbol}/bollinger-bands")
async def get_bollinger_bands(symbol: str, days: int = Query(365, ge=1, le=1000), window: int = Query(20, ge=5, le=100)):
    try:
        if not stock_service or not indicators_service:
            raise HTTPException(status_code=503, detail="Services not available")
        df = stock_service.get_historical_data(symbol.upper(), days)
        if df.empty:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")
        prices = df['Close'].tolist()
        upper_bb, middle_bb, lower_bb = indicators_service.calculate_bollinger_bands(prices, window)
        logger.info(f"Calculated Bollinger Bands for {symbol}")
        return {"symbol": symbol.upper(), "indicator": "bollinger_bands", "window": window, "upper_band": upper_bb, "middle_band": middle_bb, "lower_band": lower_bb, "prices": prices, "data_points": len(prices), "timestamp": datetime.now().isoformat()}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/signals/{symbol}")
async def get_signals(symbol: str, days: int = Query(365, ge=1, le=1000)):
    try:
        if not stock_service or not indicators_service or not signals_service:
            raise HTTPException(status_code=503, detail="Services not available")
        df = stock_service.get_historical_data(symbol.upper(), days)
        if df.empty:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")
        indicators = indicators_service.get_all_indicators(df)
        if not indicators:
            raise HTTPException(status_code=500, detail="Error calculating indicators")
        signal_data = signals_service.generate_signal(indicators)
        logger.info(f"Generated {signal_data['signal']} signal for {symbol}")
        return {"symbol": symbol.upper(), "signal": signal_data['signal'], "confidence": round(signal_data['confidence'], 2), "reasons": signal_data['reasons'], "analysis": signal_data['analysis'], "timestamp": datetime.now().isoformat()}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/portfolio/")
async def get_portfolio():
    try:
        if not portfolio_service:
            raise HTTPException(status_code=503, detail="Portfolio service not available")
        portfolio = portfolio_service.get_portfolio()
        logger.info(f"Retrieved portfolio with {len(portfolio.positions)} positions")
        return {"positions": [{"symbol": p.symbol, "quantity": p.quantity, "buy_price": p.buy_price, "current_price": p.current_price, "buy_date": p.buy_date.isoformat(), "current_value": (p.current_price * p.quantity), "gain_loss": (p.current_price * p.quantity) - (p.buy_price * p.quantity), "gain_loss_percent": ((p.current_price - p.buy_price) / p.buy_price * 100)} for p in portfolio.positions], "total_value": portfolio.total_value, "total_invested": portfolio.total_invested, "total_gain_loss": portfolio.total_gain_loss, "total_gain_loss_percent": portfolio.total_gain_loss_percent, "timestamp": datetime.now().isoformat()}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/api/portfolio/add")
async def add_position(symbol: str, quantity: float, buy_price: float):
    try:
        if not portfolio_service:
            raise HTTPException(status_code=503, detail="Portfolio service not available")
        if quantity <= 0 or buy_price <= 0:
            raise HTTPException(status_code=400, detail="Quantity and price must be positive")
        success = portfolio_service.add_position(symbol.upper(), quantity, buy_price)
        if not success:
            raise HTTPException(status_code=400, detail="Failed to add position")
        logger.info(f"Added position: {quantity} shares of {symbol}")
        return {"message": f"Successfully added {quantity} shares of {symbol} at ${buy_price}", "symbol": symbol.upper(), "quantity": quantity, "buy_price": buy_price, "total_cost": quantity * buy_price, "timestamp": datetime.now().isoformat()}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.delete("/api/portfolio/{symbol}")
async def remove_position(symbol: str):
    try:
        if not portfolio_service:
            raise HTTPException(status_code=503, detail="Portfolio service not available")
        success = portfolio_service.remove_position(symbol.upper())
        if not success:
            raise HTTPException(status_code=404, detail=f"Position {symbol} not found")
        logger.info(f"Removed position: {symbol}")
        return {"message": f"Successfully removed {symbol} from portfolio", "symbol": symbol.upper(), "timestamp": datetime.now().isoformat()}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/portfolio/metrics/summary")
async def get_portfolio_metrics():
    try:
        if not portfolio_service:
            raise HTTPException(status_code=503, detail="Portfolio service not available")
        metrics = portfolio_service.get_metrics()
        logger.info("Retrieved portfolio metrics")
        return {"total_value": metrics.total_value, "total_invested": metrics.total_invested, "total_gain_loss": metrics.total_gain_loss, "total_gain_loss_percent": metrics.total_gain_loss_percent, "timestamp": datetime.now().isoformat()}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/api/ai/query")
async def query_ai(question: str, symbol: str = None):
    try:
        if not ai_service:
            raise HTTPException(status_code=503, detail="AI service not available")
        if not question or len(question.strip()) == 0:
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        response = ai_service.process_query(question, symbol)
        logger.info(f"Processed AI query for symbol: {symbol}")
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/indian/stocks/list")
async def get_indian_stocks_list():
    try:
        if not indian_stock_service:
            raise HTTPException(status_code=503, detail="Indian stock service not available")
        stocks = list(indian_stock_service.indian_stocks.keys())
        logger.info(f"Retrieved list of {len(stocks)} Indian stocks")
        return {"stocks": stocks, "total": len(stocks), "timestamp": datetime.now().isoformat()}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/indian/stocks/{symbol}")
async def get_indian_stock_data(symbol: str, days: int = Query(365, ge=1, le=1000)):
    try:
        if not indian_stock_service:
            raise HTTPException(status_code=503, detail="Indian stock service not available")
        if not indian_stock_service.validate_indian_symbol(symbol.upper()):
            raise HTTPException(status_code=404, detail=f"Indian stock symbol {symbol} not found")
        df = indian_stock_service.get_indian_stock_historical_data(symbol.upper(), days)
        if df.empty:
            raise HTTPException(status_code=404, detail=f"No data found for Indian stock {symbol}")
        latest_price = df['Close'].iloc[-1]
        prices = [{"date": idx.isoformat(), "open": float(row['Open']), "high": float(row['High']), "low": float(row['Low']), "close": float(row['Close']), "volume": int(row['Volume'])} for idx, row in df.iterrows()]
        logger.info(f"Retrieved {len(prices)} days of data for Indian stock {symbol}")
        return {"symbol": symbol.upper(), "prices": prices, "current_price_inr": float(latest_price), "currency": "INR", "exchange": "NSE", "last_updated": datetime.now().isoformat(), "data_points": len(prices)}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/indian/stocks/{symbol}/latest")
async def get_indian_stock_latest_price(symbol: str):
    try:
        if not indian_stock_service:
            raise HTTPException(status_code=503, detail="Indian stock service not available")
        latest_price = indian_stock_service.get_indian_stock_price(symbol.upper())
        if latest_price is None:
            raise HTTPException(status_code=404, detail=f"No data found for Indian stock {symbol}")
        stock_info = indian_stock_service.get_indian_stock_info(symbol.upper())
        logger.info(f"Retrieved latest price for Indian stock {symbol}: ₹{latest_price}")
        return {"symbol": symbol.upper(), "price_inr": latest_price, "currency": "INR", "exchange": "NSE", "name": stock_info.get("name"), "sector": stock_info.get("sector"), "timestamp": datetime.now().isoformat()}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error", "error": str(exc), "timestamp": datetime.now().isoformat()})

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Stock AI Technical Analyst API v1.0.0")
    logger.info(f"Services available: Stock={stock_service is not None}, Indicators={indicators_service is not None}")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")