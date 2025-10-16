from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Stock AI Technical Analyst API", description="A comprehensive AI-powered stock technical analysis assistant", version="1.0.0", docs_url="/docs", redoc_url="/redoc", openapi_url="/openapi.json")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
async def root():
    return {"message": "Welcome to Stock AI Technical Analyst API", "version": "1.0.0", "documentation": "/docs", "status": "active"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Stock AI Technical Analyst API", "version": "1.0.0"}

@app.get("/api/stocks/{symbol}")
async def get_stock_data(symbol: str, days: int = 365):
    try:
        return {"symbol": symbol, "days": days, "message": "Stock data endpoint", "status": "available"}
    except Exception as e:
        logger.error(f"Error fetching stock data for {symbol}: {str(e)}")
        return {"error": str(e)}

@app.get("/api/stocks/{symbol}/latest")
async def get_latest_price(symbol: str):
    try:
        return {"symbol": symbol, "message": "Latest price endpoint", "status": "available"}
    except Exception as e:
        logger.error(f"Error fetching latest price for {symbol}: {str(e)}")
        return {"error": str(e)}

@app.get("/api/indicators/{symbol}")
async def get_indicators(symbol: str, window: int = 20):
    try:
        return {"symbol": symbol, "window": window, "indicators": ["moving_average", "rsi", "macd", "bollinger_bands"], "status": "available"}
    except Exception as e:
        logger.error(f"Error calculating indicators for {symbol}: {str(e)}")
        return {"error": str(e)}

@app.get("/api/indicators/{symbol}/moving-average")
async def get_moving_average(symbol: str, window: int = 20):
    try:
        return {"symbol": symbol, "indicator": "moving_average", "window": window, "status": "available"}
    except Exception as e:
        logger.error(f"Error calculating moving average: {str(e)}")
        return {"error": str(e)}

@app.get("/api/indicators/{symbol}/rsi")
async def get_rsi(symbol: str, window: int = 14):
    try:
        return {"symbol": symbol, "indicator": "rsi", "window": window, "status": "available"}
    except Exception as e:
        logger.error(f"Error calculating RSI: {str(e)}")
        return {"error": str(e)}

@app.get("/api/indicators/{symbol}/macd")
async def get_macd(symbol: str):
    try:
        return {"symbol": symbol, "indicator": "macd", "status": "available"}
    except Exception as e:
        logger.error(f"Error calculating MACD: {str(e)}")
        return {"error": str(e)}

@app.get("/api/indicators/{symbol}/bollinger-bands")
async def get_bollinger_bands(symbol: str, window: int = 20):
    try:
        return {"symbol": symbol, "indicator": "bollinger_bands", "window": window, "status": "available"}
    except Exception as e:
        logger.error(f"Error calculating Bollinger Bands: {str(e)}")
        return {"error": str(e)}

@app.get("/api/signals/{symbol}")
async def get_signals(symbol: str):
    try:
        return {"symbol": symbol, "message": "Trading signals endpoint", "status": "available"}
    except Exception as e:
        logger.error(f"Error generating signals: {str(e)}")
        return {"error": str(e)}

@app.get("/api/signals/{symbol}/recommendation")
async def get_recommendation(symbol: str):
    try:
        return {"symbol": symbol, "message": "Trading recommendation endpoint", "status": "available"}
    except Exception as e:
        logger.error(f"Error getting recommendation: {str(e)}")
        return {"error": str(e)}

@app.get("/api/portfolio/")
async def get_portfolio():
    try:
        return {"message": "Portfolio retrieval endpoint", "status": "available"}
    except Exception as e:
        logger.error(f"Error retrieving portfolio: {str(e)}")
        return {"error": str(e)}

@app.post("/api/portfolio/add")
async def add_position(symbol: str, quantity: float, buy_price: float):
    try:
        return {"message": f"Added {quantity} shares of {symbol} at ${buy_price}", "status": "available"}
    except Exception as e:
        logger.error(f"Error adding position: {str(e)}")
        return {"error": str(e)}

@app.delete("/api/portfolio/{symbol}")
async def remove_position(symbol: str):
    try:
        return {"message": f"Removed {symbol} from portfolio", "status": "available"}
    except Exception as e:
        logger.error(f"Error removing position: {str(e)}")
        return {"error": str(e)}

@app.get("/api/portfolio/metrics/summary")
async def get_portfolio_metrics():
    try:
        return {"message": "Portfolio metrics endpoint", "status": "available"}
    except Exception as e:
        logger.error(f"Error calculating metrics: {str(e)}")
        return {"error": str(e)}

@app.post("/api/ai/query")
async def query_ai(question: str, symbol: str = None):
    try:
        return {"question": question, "symbol": symbol, "message": "AI query endpoint", "status": "available"}
    except Exception as e:
        logger.error(f"Error processing AI query: {str(e)}")
        return {"error": str(e)}

@app.get("/api/ai/analysis/{symbol}")
async def get_ai_analysis(symbol: str):
    try:
        return {"symbol": symbol, "message": "AI analysis endpoint", "status": "available"}
    except Exception as e:
        logger.error(f"Error generating AI analysis: {str(e)}")
        return {"error": str(e)}

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error", "error": str(exc)})

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Stock AI Technical Analyst API...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
