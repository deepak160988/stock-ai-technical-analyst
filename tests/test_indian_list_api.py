"""
Tests for Indian stocks list API endpoint
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestIndianListAPI:
    """Test cases for /api/indian/stocks/list endpoint"""
    
    def test_list_default_returns_dict_with_stocks_array(self):
        """Test that default behavior returns dict with stocks array"""
        response = client.get("/api/indian/stocks/list")
        
        assert response.status_code == 200
        data = response.json()
        
        # Default response should be a dict with stocks, total, timestamp
        assert isinstance(data, dict)
        assert "stocks" in data
        assert "total" in data
        assert "timestamp" in data
        
        # stocks should be a list of strings
        assert isinstance(data["stocks"], list)
        assert len(data["stocks"]) > 0
        
        # All items should be strings (symbol keys)
        for item in data["stocks"]:
            assert isinstance(item, str)
        
        # Total should match length
        assert data["total"] == len(data["stocks"])
    
    def test_list_include_tickers_false_returns_dict(self):
        """Test that include_tickers=false returns dict (backward compatible)"""
        response = client.get("/api/indian/stocks/list?include_tickers=false")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, dict)
        assert "stocks" in data
        assert isinstance(data["stocks"], list)
    
    def test_list_include_tickers_0_returns_dict(self):
        """Test that include_tickers=0 returns dict (backward compatible)"""
        response = client.get("/api/indian/stocks/list?include_tickers=0")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, dict)
        assert "stocks" in data
        assert isinstance(data["stocks"], list)
    
    def test_list_include_tickers_true_returns_array_of_objects(self):
        """Test that include_tickers=true returns array of objects"""
        response = client.get("/api/indian/stocks/list?include_tickers=true")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should be a list of objects
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Each item should have symbol and ticker keys
        for item in data:
            assert isinstance(item, dict)
            assert "symbol" in item
            assert "ticker" in item
            assert isinstance(item["symbol"], str)
            assert isinstance(item["ticker"], str)
            # Ticker should end with .NS or .BO
            assert item["ticker"].endswith(".NS") or item["ticker"].endswith(".BO")
    
    def test_list_include_tickers_1_returns_array_of_objects(self):
        """Test that include_tickers=1 returns array of objects"""
        response = client.get("/api/indian/stocks/list?include_tickers=1")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should be a list of objects
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Each item should have symbol and ticker
        for item in data:
            assert "symbol" in item
            assert "ticker" in item
    
    def test_list_default_and_include_tickers_false_same_symbols(self):
        """Test that default and include_tickers=false return same symbols"""
        response_default = client.get("/api/indian/stocks/list")
        response_false = client.get("/api/indian/stocks/list?include_tickers=false")
        
        assert response_default.status_code == 200
        assert response_false.status_code == 200
        
        symbols_default = response_default.json()["stocks"]
        symbols_false = response_false.json()["stocks"]
        
        assert sorted(symbols_default) == sorted(symbols_false)
    
    def test_list_include_tickers_symbols_match_default(self):
        """Test that include_tickers=true symbols match default response"""
        response_default = client.get("/api/indian/stocks/list")
        response_with_tickers = client.get("/api/indian/stocks/list?include_tickers=true")
        
        assert response_default.status_code == 200
        assert response_with_tickers.status_code == 200
        
        symbols_default = set(response_default.json()["stocks"])
        symbols_with_tickers = set(item["symbol"] for item in response_with_tickers.json())
        
        assert symbols_default == symbols_with_tickers
    
    def test_list_returns_multiple_symbols(self):
        """Test that list returns a significant number of symbols"""
        response = client.get("/api/indian/stocks/list")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should have at least 50 symbols
        assert len(data["stocks"]) >= 50
    
    def test_list_include_tickers_ticker_format(self):
        """Test that tickers in include_tickers response are properly formatted"""
        response = client.get("/api/indian/stocks/list?include_tickers=1")
        
        assert response.status_code == 200
        data = response.json()
        
        for item in data:
            ticker = item["ticker"]
            # Should be uppercase
            assert ticker == ticker.upper()
            # Should end with .NS or .BO
            assert ticker.endswith(".NS") or ticker.endswith(".BO")
    
    def test_list_no_duplicates(self):
        """Test that default list has no duplicate symbols"""
        response = client.get("/api/indian/stocks/list")
        
        assert response.status_code == 200
        stocks = response.json()["stocks"]
        
        # Check no duplicates
        assert len(stocks) == len(set(stocks))
    
    def test_list_include_tickers_no_duplicates(self):
        """Test that include_tickers list has no duplicate symbols"""
        response = client.get("/api/indian/stocks/list?include_tickers=true")
        
        assert response.status_code == 200
        data = response.json()
        
        symbols = [item["symbol"] for item in data]
        
        # Check no duplicates
        assert len(symbols) == len(set(symbols))
