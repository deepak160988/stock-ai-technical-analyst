"""
Integration tests for API endpoints with timeframe support
"""

import pytest
import sys
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)


def create_mock_dataframe(days=30):
    """Create a mock DataFrame that simulates stock data"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    data = {
        'Open': np.random.uniform(100, 200, days),
        'High': np.random.uniform(100, 200, days),
        'Low': np.random.uniform(100, 200, days),
        'Close': np.random.uniform(100, 200, days),
        'Volume': np.random.randint(1000000, 10000000, days),
    }
    return pd.DataFrame(data, index=dates)


class TestStockAPIWithTimeframe:
    """Integration tests for stock API endpoints with timeframe parameter"""
    
    @patch('services.stock_service.StockService.validate_symbol')
    @patch('services.stock_service.StockService.get_historical_data')
    def test_get_stock_data_with_valid_timeframe_1d(self, mock_get_data, mock_validate):
        """Test GET /api/stocks/{symbol} with valid 1d timeframe"""
        mock_validate.return_value = True
        mock_get_data.return_value = create_mock_dataframe(30)
        
        response = client.get("/api/stocks/AAPL?timeframe=1d")
        assert response.status_code == 200
        data = response.json()
        assert "symbol" in data
        assert data["symbol"] == "AAPL"
        assert "prices" in data
        assert "timeframe" in data
        assert data["timeframe"] == "1d"
        assert len(data["prices"]) > 0
    
    @patch('services.stock_service.StockService.validate_symbol')
    @patch('services.stock_service.StockService.get_historical_data')
    def test_get_stock_data_with_valid_timeframe_1h(self, mock_get_data, mock_validate):
        """Test GET /api/stocks/{symbol} with valid 1h timeframe"""
        mock_validate.return_value = True
        mock_get_data.return_value = create_mock_dataframe(50)
        
        response = client.get("/api/stocks/AAPL?timeframe=1h")
        assert response.status_code == 200
        data = response.json()
        assert "symbol" in data
        assert data["symbol"] == "AAPL"
        assert "timeframe" in data
        assert data["timeframe"] == "1h"
    
    @patch('services.stock_service.StockService.validate_symbol')
    @patch('services.stock_service.StockService.get_historical_data')
    def test_get_stock_data_with_valid_timeframe_1m(self, mock_get_data, mock_validate):
        """Test GET /api/stocks/{symbol} with valid 1m timeframe"""
        mock_validate.return_value = True
        mock_get_data.return_value = create_mock_dataframe(100)
        
        response = client.get("/api/stocks/AAPL?timeframe=1m")
        assert response.status_code == 200
        data = response.json()
        assert "symbol" in data
        assert data["symbol"] == "AAPL"
        assert "timeframe" in data
        assert data["timeframe"] == "1m"
    
    def test_get_stock_data_with_invalid_timeframe(self):
        """Test GET /api/stocks/{symbol} with invalid timeframe returns 400"""
        response = client.get("/api/stocks/AAPL?timeframe=2h")
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Invalid timeframe" in data["detail"]
    
    @patch('services.stock_service.StockService.validate_symbol')
    @patch('services.stock_service.StockService.get_historical_data')
    def test_get_stock_data_without_timeframe(self, mock_get_data, mock_validate):
        """Test GET /api/stocks/{symbol} without timeframe parameter (backward compatibility)"""
        mock_validate.return_value = True
        mock_get_data.return_value = create_mock_dataframe(30)
        
        response = client.get("/api/stocks/AAPL?days=30")
        assert response.status_code == 200
        data = response.json()
        assert "symbol" in data
        assert data["symbol"] == "AAPL"
        # When no timeframe specified, it should still work with days parameter
        assert "prices" in data
        assert len(data["prices"]) > 0


class TestIndianStockAPIWithTimeframe:
    """Integration tests for Indian stock API endpoints with timeframe parameter"""
    
    @patch('services.indian_stock_service.IndianStockService.validate_indian_symbol')
    @patch('services.indian_stock_service.IndianStockService.get_indian_stock_historical_data')
    def test_get_indian_stock_data_with_valid_timeframe_1d(self, mock_get_data, mock_validate):
        """Test GET /api/indian/stocks/{symbol} with valid 1d timeframe"""
        mock_validate.return_value = True
        mock_get_data.return_value = create_mock_dataframe(30)
        
        response = client.get("/api/indian/stocks/RELIANCE?timeframe=1d")
        assert response.status_code == 200
        data = response.json()
        assert "symbol" in data
        assert data["symbol"] == "RELIANCE"
        assert "prices" in data
        assert "timeframe" in data
        assert data["timeframe"] == "1d"
        assert "currency" in data
        assert data["currency"] == "INR"
    
    @patch('services.indian_stock_service.IndianStockService.validate_indian_symbol')
    @patch('services.indian_stock_service.IndianStockService.get_indian_stock_historical_data')
    def test_get_indian_stock_data_with_valid_timeframe_1h(self, mock_get_data, mock_validate):
        """Test GET /api/indian/stocks/{symbol} with valid 1h timeframe"""
        mock_validate.return_value = True
        mock_get_data.return_value = create_mock_dataframe(50)
        
        response = client.get("/api/indian/stocks/TCS?timeframe=1h")
        assert response.status_code == 200
        data = response.json()
        assert "symbol" in data
        assert data["symbol"] == "TCS"
        assert "timeframe" in data
        assert data["timeframe"] == "1h"
    
    def test_get_indian_stock_data_with_invalid_timeframe(self):
        """Test GET /api/indian/stocks/{symbol} with invalid timeframe returns 400"""
        response = client.get("/api/indian/stocks/RELIANCE?timeframe=invalid")
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Invalid timeframe" in data["detail"]
    
    @patch('services.indian_stock_service.IndianStockService.validate_indian_symbol')
    @patch('services.indian_stock_service.IndianStockService.get_indian_stock_historical_data')
    def test_get_indian_stock_data_without_timeframe(self, mock_get_data, mock_validate):
        """Test GET /api/indian/stocks/{symbol} without timeframe (backward compatibility)"""
        mock_validate.return_value = True
        mock_get_data.return_value = create_mock_dataframe(30)
        
        response = client.get("/api/indian/stocks/RELIANCE?days=30")
        assert response.status_code == 200
        data = response.json()
        assert "symbol" in data
        assert data["symbol"] == "RELIANCE"
        assert "prices" in data


class TestTimeframeValidation:
    """Test timeframe validation across all supported values"""
    
    @pytest.mark.parametrize("timeframe", [
        "1m", "3m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1mo"
    ])
    @patch('services.stock_service.StockService.validate_symbol')
    @patch('services.stock_service.StockService.get_historical_data')
    def test_all_valid_timeframes(self, mock_get_data, mock_validate, timeframe):
        """Test that all allowed timeframes work correctly"""
        mock_validate.return_value = True
        mock_get_data.return_value = create_mock_dataframe(30)
        
        response = client.get(f"/api/stocks/AAPL?timeframe={timeframe}")
        assert response.status_code == 200
        data = response.json()
        assert data["timeframe"] == timeframe
    
    @pytest.mark.parametrize("timeframe", [
        "2m", "10m", "2h", "6h", "2d", "3w", "2mo", "invalid", "abc"
    ])
    def test_all_invalid_timeframes(self, timeframe):
        """Test that invalid timeframes return 400 error"""
        response = client.get(f"/api/stocks/AAPL?timeframe={timeframe}")
        assert response.status_code == 400
        data = response.json()
        assert "Invalid timeframe" in data["detail"]
