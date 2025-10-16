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

# Initialize FastAPI app
app = FastAPI(
    title="Stock AI Technical Analyst API",
    version="1.0.0",
    description="Advanced stock analysis with technical indicators and ML predictions"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

logger.info("=" * 80)
logger.info("Starting Stock AI Technical Analyst API v1.0.0")
logger.info("User: deepak160988")
logger.info("=" * 80)

# ============== ROOT ENDPOINTS ==============
@app.get("/")
async def root():
    return {
        "message": "Welcome to Stock AI Technical Analyst API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Stock AI Technical Analyst API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

# ============== STOCK ENDPOINTS ==============
@app.get("/api/stocks/{symbol}")
async def get_stock_data(symbol: str, days: int = Query(365, ge=1, le=1000)):
    try:
        logger.info(f"Fetching stock data for {symbol}")
        # Mock data for testing
        return {
            "symbol": symbol.upper(),
            "current_price": 150.25,
            "currency": "USD",
            "data_points": days,
            "prices": [
                {
                    "date": f"2025-10-{16+i:02d}",
                    "open": 150.0 + i*0.1,
                    "high": 151.0 + i*0.1,
                    "low": 149.0 + i*0.1,
                    "close": 150.25 + i*0.1,
                    "volume": 1000000
                }
                for i in range(min(5, days))
            ],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stocks/{symbol}/latest")
async def get_latest_price(symbol: str):
    try:
        logger.info(f"Fetching latest price for {symbol}")
        return {
            "symbol": symbol.upper(),
            "price": 150.25,
            "currency": "USD",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============== INDICATORS ENDPOINTS ==============
@app.get("/api/indicators/{symbol}")
async def get_indicators(symbol: str, days: int = Query(365, ge=1, le=1000)):
    try:
        logger.info(f"Fetching indicators for {symbol}")
        return {
            "symbol": symbol.upper(),
            "indicators": {
                "rsi": 65.5,
                "macd": 2.5,
                "bollinger_bands": {"upper": 155, "middle": 150, "lower": 145}
            },
            "data_points": days,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/indicators/{symbol}/rsi")
async def get_rsi(symbol: str, days: int = Query(365, ge=1, le=1000), window: int = Query(14, ge=5, le=100)):
    try:
        logger.info(f"Fetching RSI for {symbol}")
        return {
            "symbol": symbol.upper(),
            "indicator": "rsi",
            "window": window,
            "values": [50 + i*2 for i in range(10)],
            "latest_rsi": 65.5,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/indicators/{symbol}/macd")
async def get_macd(symbol: str, days: int = Query(365, ge=1, le=1000)):
    try:
        logger.info(f"Fetching MACD for {symbol}")
        return {
            "symbol": symbol.upper(),
            "indicator": "macd",
            "macd_line": [2.0 + i*0.1 for i in range(10)],
            "signal_line": [1.8 + i*0.1 for i in range(10)],
            "histogram": [0.2 + i*0.05 for i in range(10)],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/indicators/{symbol}/bollinger-bands")
async def get_bollinger_bands(symbol: str, days: int = Query(365, ge=1, le=1000), window: int = Query(20, ge=5, le=100)):
    try:
        logger.info(f"Fetching Bollinger Bands for {symbol}")
        return {
            "symbol": symbol.upper(),
            "indicator": "bollinger_bands",
            "window": window,
            "upper_band": [155 + i*0.1 for i in range(10)],
            "middle_band": [150 + i*0.1 for i in range(10)],
            "lower_band": [145 + i*0.1 for i in range(10)],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============== SIGNALS ENDPOINTS ==============
@app.get("/api/signals/{symbol}")
async def get_signals(symbol: str, days: int = Query(365, ge=1, le=1000)):
    try:
        logger.info(f"Generating signal for {symbol}")
        return {
            "symbol": symbol.upper(),
            "signal": "BUY",
            "confidence": 0.85,
            "reasons": ["RSI is oversold", "MACD crossover", "Bollinger Bands bounce"],
            "analysis": "Strong buy signal detected",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============== ML PREDICTION ENDPOINTS ==============
@app.get("/api/ml/predict")
async def ml_predict(symbol: str, days: int = Query(7, ge=1, le=30)):
    try:
        logger.info(f"Generating ML prediction for {symbol}")
        return {
            "symbol": symbol.upper(),
            "current_price": 150.25,
            "predicted_price": 155.50,
            "confidence": 0.82,
            "model_accuracy": 0.78,
            "prediction_date": datetime.now().isoformat(),
            "forecast_days": days,
            "trend": "UPWARD",
            "price_change_percent": 3.5
        }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============== PORTFOLIO ENDPOINTS ==============
@app.get("/api/portfolio/")
async def get_portfolio():
    try:
        logger.info("Fetching portfolio")
        return {
            "positions": [
                {
                    "symbol": "AAPL",
                    "quantity": 10,
                    "buy_price": 140.0,
                    "current_price": 150.25,
                    "current_value": 1502.5,
                    "gain_loss": 102.5,
                    "gain_loss_percent": 7.32
                }
            ],
            "total_value": 1502.5,
            "total_invested": 1400.0,
            "total_gain_loss": 102.5,
            "total_gain_loss_percent": 7.32,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============== INDIAN STOCKS ENDPOINTS ==============
@app.get("/api/indian/stocks/list")
async def get_indian_stocks_list():
    try:
        logger.info("Fetching Indian stocks list")
        return {
            "stocks": ["RELIANCE", "TCS", "INFY", "WIPRO", "HDFCBANK", "ICICIBANK", "SBIN", "ITC"],
            "total": 8,
            "exchange": "NSE",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/indian/stocks/{symbol}")
async def get_indian_stock_data(symbol: str, days: int = Query(365, ge=1, le=1000)):
    try:
        logger.info(f"Fetching Indian stock data for {symbol}")
        return {
            "symbol": symbol.upper(),
            "exchange": "NSE",
            "currency": "INR",
            "current_price_inr": 2500.50,
            "data_points": days,
            "prices": [
                {
                    "date": f"2025-10-{16+i:02d}",
                    "open": 2500.0 + i*1.0,
                    "high": 2510.0 + i*1.0,
                    "low": 2490.0 + i*1.0,
                    "close": 2500.50 + i*1.0,
                    "volume": 5000000
                }
                for i in range(min(5, days))
            ],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============== EXCEPTION HANDLER ==============
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc), "timestamp": datetime.now().isoformat()}
    )

# ============== STARTUP ==============
if __name__ == "__main__":
    import uvicorn
    logger.info("=" * 80)
    logger.info("Stock AI Technical Analyst API")
    logger.info("=" * 80)
    logger.info("API Documentation available at http://localhost:8000/docs")
    logger.info("=" * 80)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
