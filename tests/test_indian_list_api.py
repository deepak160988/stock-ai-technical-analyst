"""
Tests for Indian stocks list API endpoint with include_tickers flag
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
    
    def test_list_default_returns_strings(self):
        """Test that default list endpoint returns list of strings"""
        response = client.get("/api/indian/stocks/list")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert "stocks" in data
        assert "total" in data
        assert "timestamp" in data
        
        stocks = data["stocks"]
        
        # Should be a list
        assert isinstance(stocks, list)
        
        # Should have at least some stocks
        assert len(stocks) > 0
        
        # All items should be strings
        for stock in stocks:
            assert isinstance(stock, str), f"Expected string, got {type(stock)} for {stock}"
    
    def test_list_include_tickers_false_returns_strings(self):
        """Test that include_tickers=false returns list of strings"""
        response = client.get("/api/indian/stocks/list?include_tickers=false")
        
        assert response.status_code == 200
        data = response.json()
        
        stocks = data["stocks"]
        
        # Should be a list of strings
        assert isinstance(stocks, list)
        assert all(isinstance(stock, str) for stock in stocks)
    
    def test_list_include_tickers_0_returns_strings(self):
        """Test that include_tickers=0 returns list of strings"""
        response = client.get("/api/indian/stocks/list?include_tickers=0")
        
        assert response.status_code == 200
        data = response.json()
        
        stocks = data["stocks"]
        
        # Should be a list of strings
        assert isinstance(stocks, list)
        assert all(isinstance(stock, str) for stock in stocks)
    
    def test_list_include_tickers_true_returns_objects(self):
        """Test that include_tickers=true returns list of objects"""
        response = client.get("/api/indian/stocks/list?include_tickers=true")
        
        assert response.status_code == 200
        data = response.json()
        
        stocks = data["stocks"]
        
        # Should be a list
        assert isinstance(stocks, list)
        
        # Should have at least some stocks
        assert len(stocks) > 0
        
        # All items should be objects with symbol and ticker keys
        for stock in stocks:
            assert isinstance(stock, dict), f"Expected dict, got {type(stock)} for {stock}"
            assert "symbol" in stock, f"Missing 'symbol' key in {stock}"
            assert "ticker" in stock, f"Missing 'ticker' key in {stock}"
            
            # Values should be strings
            assert isinstance(stock["symbol"], str)
            assert isinstance(stock["ticker"], str)
            
            # Ticker should end with .NS or .BO
            assert stock["ticker"].endswith(".NS") or stock["ticker"].endswith(".BO"), \
                f"Invalid ticker format: {stock['ticker']}"
    
    def test_list_include_tickers_1_returns_objects(self):
        """Test that include_tickers=1 returns list of objects"""
        response = client.get("/api/indian/stocks/list?include_tickers=1")
        
        assert response.status_code == 200
        data = response.json()
        
        stocks = data["stocks"]
        
        # Should be a list of objects
        assert isinstance(stocks, list)
        assert all(isinstance(stock, dict) for stock in stocks)
        assert all("symbol" in stock and "ticker" in stock for stock in stocks)
    
    def test_list_total_count_matches(self):
        """Test that total count matches actual list length"""
        response = client.get("/api/indian/stocks/list")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["total"] == len(data["stocks"])
    
    def test_list_include_tickers_total_count_matches(self):
        """Test that total count matches with include_tickers"""
        response = client.get("/api/indian/stocks/list?include_tickers=true")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["total"] == len(data["stocks"])
    
    def test_list_backward_compatibility(self):
        """Test that default behavior is backward compatible"""
        # Default should return same format as before
        response_default = client.get("/api/indian/stocks/list")
        response_explicit = client.get("/api/indian/stocks/list?include_tickers=false")
        
        assert response_default.status_code == 200
        assert response_explicit.status_code == 200
        
        default_stocks = response_default.json()["stocks"]
        explicit_stocks = response_explicit.json()["stocks"]
        
        # Both should return list of strings
        assert all(isinstance(s, str) for s in default_stocks)
        assert all(isinstance(s, str) for s in explicit_stocks)
    
    def test_list_symbols_are_uppercase(self):
        """Test that all symbols are uppercase"""
        response = client.get("/api/indian/stocks/list")
        
        assert response.status_code == 200
        data = response.json()
        
        stocks = data["stocks"]
        
        for stock in stocks:
            assert stock == stock.upper(), f"Symbol {stock} is not uppercase"
    
    def test_list_include_tickers_symbols_are_uppercase(self):
        """Test that all symbols are uppercase with include_tickers"""
        response = client.get("/api/indian/stocks/list?include_tickers=true")
        
        assert response.status_code == 200
        data = response.json()
        
        stocks = data["stocks"]
        
        for stock in stocks:
            assert stock["symbol"] == stock["symbol"].upper(), \
                f"Symbol {stock['symbol']} is not uppercase"
