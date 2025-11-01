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
    """Test cases for Indian stocks search endpoint"""

    def test_search_hdfc_returns_matches(self):
        """Test that query=HDFC returns at least one of [HDFC, HDFCBANK, HDFCLIFE, HDFCAMC]"""
        response = client.get("/api/indian/stocks/search?query=HDFC")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "query" in data
        assert "results" in data
        assert "total" in data
        assert "timestamp" in data
        
        assert data["query"] == "HDFC"
        assert isinstance(data["results"], list)
        assert data["total"] == len(data["results"])
        
        # Should have at least one of these symbols
        expected_matches = ["HDFC", "HDFCBANK", "HDFCLIFE", "HDFCAMC"]
        found_matches = [s for s in expected_matches if s in data["results"]]
        assert len(found_matches) > 0, f"Expected at least one of {expected_matches}, got {data['results']}"

    def test_search_tcs_ns_returns_tcs(self):
        """Test that query=TCS.NS returns TCS"""
        response = client.get("/api/indian/stocks/search?query=TCS.NS")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "TCS" in data["results"], f"Expected TCS in results, got {data['results']}"

    def test_search_empty_query_returns_400(self):
        """Test that empty query returns 400 error"""
        response = client.get("/api/indian/stocks/search?query=")
        
        assert response.status_code == 422  # FastAPI validation error for min_length=1

    def test_search_case_insensitive(self):
        """Test that search is case-insensitive"""
        response_upper = client.get("/api/indian/stocks/search?query=RELIANCE")
        response_lower = client.get("/api/indian/stocks/search?query=reliance")
        
        assert response_upper.status_code == 200
        assert response_lower.status_code == 200
        
        data_upper = response_upper.json()
        data_lower = response_lower.json()
        
        # Both should return the same results (RELIANCE should be in both)
        assert "RELIANCE" in data_upper["results"]
        assert "RELIANCE" in data_lower["results"]

    def test_search_partial_match(self):
        """Test that partial matches work"""
        response = client.get("/api/indian/stocks/search?query=ADANI")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should find multiple ADANI stocks
        adani_stocks = [s for s in data["results"] if "ADANI" in s]
        assert len(adani_stocks) > 0, "Expected to find ADANI stocks"

    def test_search_no_matches(self):
        """Test that search with no matches returns empty list"""
        response = client.get("/api/indian/stocks/search?query=ZZZZZZZ")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["results"] == []
        assert data["total"] == 0

    def test_search_max_length_validation(self):
        """Test that query longer than 50 chars returns validation error"""
        long_query = "A" * 51
        response = client.get(f"/api/indian/stocks/search?query={long_query}")
        
        assert response.status_code == 422  # FastAPI validation error

    def test_search_response_structure(self):
        """Test that response has correct structure"""
        response = client.get("/api/indian/stocks/search?query=TCS")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check all required fields
        assert "query" in data
        assert "results" in data
        assert "total" in data
        assert "timestamp" in data
        
        # Check types
        assert isinstance(data["query"], str)
        assert isinstance(data["results"], list)
        assert isinstance(data["total"], int)
        assert isinstance(data["timestamp"], str)

    def test_list_endpoint_unchanged(self):
        """Test that the list endpoint still works and returns all stocks"""
        response = client.get("/api/indian/stocks/list")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "stocks" in data
        assert "total" in data
        assert "timestamp" in data
        
        # Should have at least 100 stocks (expanded coverage)
        assert data["total"] >= 100
        assert len(data["stocks"]) == data["total"]
