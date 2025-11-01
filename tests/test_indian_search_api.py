"""
Tests for Indian stocks search API endpoint
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestIndianSearchAPI:
    """Test cases for /api/indian/stocks/search endpoint"""
    
    def test_search_hdfc_returns_results(self):
        """Test that searching for HDFC returns at least one relevant result"""
        response = client.get("/api/indian/stocks/search?query=HDFC")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert "query" in data
        assert "results" in data
        assert "total" in data
        assert "timestamp" in data
        
        # Query should be preserved
        assert data["query"] == "HDFC"
        
        # Should return at least one of the HDFC-related symbols
        expected_symbols = ["HDFC", "HDFCBANK", "HDFCLIFE", "HDFCAMC"]
        results = data["results"]
        
        assert len(results) > 0, "Search for HDFC should return at least one result"
        
        # At least one of the expected symbols should be present
        assert any(symbol in results for symbol in expected_symbols), \
            f"Expected at least one of {expected_symbols} in results, got {results}"
    
    def test_search_tcs_ticker_returns_tcs(self):
        """Test that searching for TCS.NS ticker returns TCS symbol"""
        response = client.get("/api/indian/stocks/search?query=TCS.NS")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "results" in data
        results = data["results"]
        
        # Should return TCS symbol
        assert "TCS" in results, f"Expected TCS in results, got {results}"
    
    def test_search_case_insensitive(self):
        """Test that search is case-insensitive"""
        response_upper = client.get("/api/indian/stocks/search?query=RELIANCE")
        response_lower = client.get("/api/indian/stocks/search?query=reliance")
        response_mixed = client.get("/api/indian/stocks/search?query=Reliance")
        
        assert response_upper.status_code == 200
        assert response_lower.status_code == 200
        assert response_mixed.status_code == 200
        
        # All should return the same results
        results_upper = response_upper.json()["results"]
        results_lower = response_lower.json()["results"]
        results_mixed = response_mixed.json()["results"]
        
        assert results_upper == results_lower == results_mixed
    
    def test_search_blank_query_returns_400(self):
        """Test that blank query returns 400 error"""
        response = client.get("/api/indian/stocks/search?query=")
        
        assert response.status_code == 422  # FastAPI validation error for empty string
    
    def test_search_whitespace_query_returns_400(self):
        """Test that whitespace-only query returns 400 error"""
        response = client.get("/api/indian/stocks/search?query=   ")
        
        assert response.status_code == 400
        data = response.json()
        assert "blank" in data["detail"].lower() or "whitespace" in data["detail"].lower()
    
    def test_search_no_query_param_returns_422(self):
        """Test that missing query parameter returns 422 error"""
        response = client.get("/api/indian/stocks/search")
        
        assert response.status_code == 422  # FastAPI validation error
    
    def test_search_query_too_long_returns_422(self):
        """Test that query longer than 50 chars returns 422 error"""
        long_query = "a" * 51
        response = client.get(f"/api/indian/stocks/search?query={long_query}")
        
        assert response.status_code == 422  # FastAPI validation error
    
    def test_search_partial_match(self):
        """Test that partial matches work"""
        response = client.get("/api/indian/stocks/search?query=ADANI")
        
        assert response.status_code == 200
        data = response.json()
        results = data["results"]
        
        # Should return multiple ADANI-related symbols
        assert len(results) > 0
        
        # All results should contain "ADANI" in the symbol
        for result in results:
            assert "ADANI" in result, f"Result {result} doesn't contain ADANI"
    
    def test_search_no_results(self):
        """Test search with no matching results"""
        response = client.get("/api/indian/stocks/search?query=ZZZZNONEXISTENT")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["results"] == []
        assert data["total"] == 0
    
    def test_search_response_deduplicated(self):
        """Test that search results are deduplicated"""
        response = client.get("/api/indian/stocks/search?query=TCS")
        
        assert response.status_code == 200
        data = response.json()
        results = data["results"]
        
        # Results should not have duplicates
        assert len(results) == len(set(results)), "Results contain duplicates"
