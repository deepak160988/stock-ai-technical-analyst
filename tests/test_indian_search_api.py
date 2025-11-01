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
    
    def test_search_hdfc_returns_hdfc_symbols(self):
        """Test that searching for HDFC returns at least one HDFC symbol"""
        response = client.get("/api/indian/stocks/search?query=HDFC")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "query" in data
        assert "results" in data
        assert "total" in data
        assert "timestamp" in data
        
        # Verify query is preserved
        assert data["query"] == "HDFC"
        
        # Verify at least one of the expected HDFC symbols is present
        expected_hdfc_symbols = ["HDFC", "HDFCBANK", "HDFCLIFE", "HDFCAMC"]
        results = data["results"]
        
        # At least one should be present
        found = any(sym in results for sym in expected_hdfc_symbols)
        assert found, f"Expected at least one of {expected_hdfc_symbols} in {results}"
        
        # Verify total matches results length
        assert data["total"] == len(results)
    
    def test_search_tcs_ns_returns_tcs(self):
        """Test that searching for TCS.NS returns TCS symbol"""
        response = client.get("/api/indian/stocks/search?query=TCS.NS")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return TCS
        assert "TCS" in data["results"]
        assert data["query"] == "TCS.NS"
    
    def test_search_blank_query_returns_400(self):
        """Test that blank query returns 400 error"""
        response = client.get("/api/indian/stocks/search?query=")
        
        assert response.status_code == 422  # FastAPI validation error for min_length
    
    def test_search_whitespace_query_returns_400(self):
        """Test that whitespace-only query returns 400 error"""
        response = client.get("/api/indian/stocks/search?query=%20%20%20")
        
        assert response.status_code == 400
        data = response.json()
        assert "blank" in data["detail"].lower() or "whitespace" in data["detail"].lower()
    
    def test_search_case_insensitive(self):
        """Test that search is case-insensitive"""
        # Search with lowercase
        response_lower = client.get("/api/indian/stocks/search?query=tcs")
        # Search with uppercase
        response_upper = client.get("/api/indian/stocks/search?query=TCS")
        
        assert response_lower.status_code == 200
        assert response_upper.status_code == 200
        
        # Results should be the same (though query is preserved as-is)
        results_lower = response_lower.json()["results"]
        results_upper = response_upper.json()["results"]
        
        assert results_lower == results_upper
    
    def test_search_no_results(self):
        """Test search with query that should return no results"""
        response = client.get("/api/indian/stocks/search?query=XYZNONEXISTENT123")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return empty results
        assert data["results"] == []
        assert data["total"] == 0
    
    def test_search_missing_query_param(self):
        """Test that missing query parameter returns 422"""
        response = client.get("/api/indian/stocks/search")
        
        assert response.status_code == 422  # FastAPI validation error
    
    def test_search_query_too_long(self):
        """Test that query exceeding max_length returns 422"""
        long_query = "A" * 51  # Max is 50
        response = client.get(f"/api/indian/stocks/search?query={long_query}")
        
        assert response.status_code == 422  # FastAPI validation error
