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
        """Test that searching for HDFC returns at least one of the expected symbols"""
        response = client.get("/api/indian/stocks/search?query=HDFC")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "query" in data
        assert "results" in data
        assert "total" in data
        assert "timestamp" in data
        
        # Should return at least one of these symbols
        expected_symbols = ["HDFC", "HDFCBANK", "HDFCLIFE", "HDFCAMC"]
        results = data["results"]
        
        found = any(symbol in results for symbol in expected_symbols)
        assert found, f"Expected at least one of {expected_symbols}, got {results}"
        assert data["total"] == len(results)
    
    def test_search_tcs_ns_returns_tcs(self):
        """Test that searching for TCS.NS returns TCS"""
        response = client.get("/api/indian/stocks/search?query=TCS.NS")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "TCS" in data["results"]
        assert data["query"] == "TCS.NS"
    
    def test_search_blank_query_returns_400(self):
        """Test that blank query returns 400"""
        # Test completely blank
        response = client.get("/api/indian/stocks/search?query=")
        assert response.status_code == 422  # FastAPI validation error for empty string
        
    def test_search_whitespace_query_returns_400(self):
        """Test that whitespace-only query returns 400"""
        response = client.get("/api/indian/stocks/search?query=%20%20%20")
        
        assert response.status_code == 400
        data = response.json()
        assert "blank" in data["detail"].lower() or "whitespace" in data["detail"].lower()
    
    def test_search_case_insensitive(self):
        """Test that search is case-insensitive"""
        response_upper = client.get("/api/indian/stocks/search?query=RELIANCE")
        response_lower = client.get("/api/indian/stocks/search?query=reliance")
        
        assert response_upper.status_code == 200
        assert response_lower.status_code == 200
        
        # Both should return the same results
        assert response_upper.json()["results"] == response_lower.json()["results"]
    
    def test_search_partial_match(self):
        """Test that partial matches work"""
        response = client.get("/api/indian/stocks/search?query=ADANI")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should find multiple Adani companies
        results = data["results"]
        assert len(results) > 0
        
        # All results should contain ADANI in the symbol
        for symbol in results:
            assert "ADANI" in symbol.upper()
    
    def test_search_no_results(self):
        """Test search with no matching results"""
        response = client.get("/api/indian/stocks/search?query=XYZNONEXISTENT")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["results"] == []
        assert data["total"] == 0
    
    def test_search_query_too_long(self):
        """Test that query longer than 50 chars is rejected"""
        long_query = "A" * 51
        response = client.get(f"/api/indian/stocks/search?query={long_query}")
        
        assert response.status_code == 422  # FastAPI validation error
    
    def test_search_returns_deduplicated_results(self):
        """Test that results are de-duplicated"""
        response = client.get("/api/indian/stocks/search?query=TCS")
        
        assert response.status_code == 200
        data = response.json()
        
        results = data["results"]
        # Check no duplicates
        assert len(results) == len(set(results))
    
    def test_search_response_structure(self):
        """Test that response has correct structure"""
        response = client.get("/api/indian/stocks/search?query=INFY")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        assert "query" in data
        assert "results" in data
        assert "total" in data
        assert "timestamp" in data
        
        # Check types
        assert isinstance(data["query"], str)
        assert isinstance(data["results"], list)
        assert isinstance(data["total"], int)
        assert isinstance(data["timestamp"], str)
