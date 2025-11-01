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
    
    def test_list_default_returns_symbol_strings(self):
        """Test that default list endpoint returns list of symbol strings"""
        response = client.get("/api/indian/stocks/list")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "stocks" in data
        assert "total" in data
        assert "timestamp" in data
        
        # Verify stocks is a list
        assert isinstance(data["stocks"], list)
        
        # Verify all items are strings (not objects)
        if len(data["stocks"]) > 0:
            assert all(isinstance(stock, str) for stock in data["stocks"])
        
        # Verify total matches stocks length
        assert data["total"] == len(data["stocks"])
        
        # Should have at least some stocks
        assert len(data["stocks"]) > 0
    
    def test_list_include_tickers_false_returns_symbol_strings(self):
        """Test that include_tickers=false returns list of symbol strings"""
        response = client.get("/api/indian/stocks/list?include_tickers=false")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify stocks is a list of strings
        assert isinstance(data["stocks"], list)
        if len(data["stocks"]) > 0:
            assert all(isinstance(stock, str) for stock in data["stocks"])
    
    def test_list_include_tickers_true_returns_objects(self):
        """Test that include_tickers=true returns list of objects with symbol and ticker"""
        response = client.get("/api/indian/stocks/list?include_tickers=true")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "stocks" in data
        assert "total" in data
        assert "timestamp" in data
        
        # Verify stocks is a list
        assert isinstance(data["stocks"], list)
        
        # Verify all items are objects with symbol and ticker keys
        if len(data["stocks"]) > 0:
            for stock in data["stocks"]:
                assert isinstance(stock, dict)
                assert "symbol" in stock
                assert "ticker" in stock
                assert isinstance(stock["symbol"], str)
                assert isinstance(stock["ticker"], str)
                # Verify ticker ends with .NS or .BO
                assert stock["ticker"].endswith('.NS') or stock["ticker"].endswith('.BO')
        
        # Verify total matches stocks length
        assert data["total"] == len(data["stocks"])
    
    def test_list_include_tickers_1_returns_objects(self):
        """Test that include_tickers=1 (numeric) returns list of objects"""
        response = client.get("/api/indian/stocks/list?include_tickers=1")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify stocks is a list of objects
        assert isinstance(data["stocks"], list)
        if len(data["stocks"]) > 0:
            for stock in data["stocks"]:
                assert isinstance(stock, dict)
                assert "symbol" in stock
                assert "ticker" in stock
    
    def test_list_include_tickers_0_returns_symbol_strings(self):
        """Test that include_tickers=0 (numeric) returns list of symbol strings"""
        response = client.get("/api/indian/stocks/list?include_tickers=0")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify stocks is a list of strings
        assert isinstance(data["stocks"], list)
        if len(data["stocks"]) > 0:
            assert all(isinstance(stock, str) for stock in data["stocks"])
    
    def test_list_backward_compatibility(self):
        """Test that default behavior is backward compatible (returns strings)"""
        response = client.get("/api/indian/stocks/list")
        
        assert response.status_code == 200
        data = response.json()
        
        # Default should return list of strings (backward compatible)
        assert isinstance(data["stocks"], list)
        if len(data["stocks"]) > 0:
            # Verify it's a string, not an object
            first_item = data["stocks"][0]
            assert isinstance(first_item, str)
            # Should not be a dict
            assert not isinstance(first_item, dict)
    
    def test_list_same_total_both_modes(self):
        """Test that total count is the same in both modes"""
        response_default = client.get("/api/indian/stocks/list")
        response_with_tickers = client.get("/api/indian/stocks/list?include_tickers=true")
        
        assert response_default.status_code == 200
        assert response_with_tickers.status_code == 200
        
        total_default = response_default.json()["total"]
        total_with_tickers = response_with_tickers.json()["total"]
        
        # Both should have the same total count
        assert total_default == total_with_tickers
