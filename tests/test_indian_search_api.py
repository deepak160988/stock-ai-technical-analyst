"""
Tests for Indian stocks search API endpoint
"""

import pytest
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestIndianSearchAPI:
    """Test cases for Indian stocks search API endpoint"""
    
    def test_search_endpoint_exists(self):
        """Test that search endpoint exists and is accessible"""
        response = client.get("/api/indian/stocks/search?query=TCS")
        assert response.status_code == 200
    
    def test_search_hdfc_returns_results(self):
        """Test search for HDFC returns at least one HDFC-related symbol"""
        response = client.get("/api/indian/stocks/search?query=HDFC")
        assert response.status_code == 200
        
        data = response.json()
        assert "results" in data
        assert "query" in data
        assert "total" in data
        assert "timestamp" in data
        
        # Should return at least one of these
        expected_matches = ["HDFC", "HDFCBANK", "HDFCLIFE", "HDFCAMC"]
        results = data["results"]
        
        # Check if at least one expected match is in results
        found = any(match in results for match in expected_matches)
        assert found, f"Expected at least one of {expected_matches} in results {results}"
        assert data["total"] == len(results)
    
    def test_search_tcs_ns_returns_tcs(self):
        """Test search for TCS.NS returns TCS symbol"""
        response = client.get("/api/indian/stocks/search?query=TCS.NS")
        assert response.status_code == 200
        
        data = response.json()
        assert "results" in data
        assert "TCS" in data["results"], "TCS should be in results when searching for TCS.NS"
    
    def test_search_tcs_returns_tcs(self):
        """Test search for TCS returns TCS symbol"""
        response = client.get("/api/indian/stocks/search?query=TCS")
        assert response.status_code == 200
        
        data = response.json()
        assert "results" in data
        assert "TCS" in data["results"], "TCS should be in results"
    
    def test_search_empty_query_returns_400(self):
        """Test that empty query returns 400 error"""
        response = client.get("/api/indian/stocks/search?query=")
        assert response.status_code == 422 or response.status_code == 400
    
    def test_search_missing_query_param_returns_422(self):
        """Test that missing query parameter returns 422 error"""
        response = client.get("/api/indian/stocks/search")
        assert response.status_code == 422
    
    def test_search_case_insensitive(self):
        """Test that search is case-insensitive"""
        response1 = client.get("/api/indian/stocks/search?query=tcs")
        response2 = client.get("/api/indian/stocks/search?query=TCS")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()
        data2 = response2.json()
        
        # Results should be the same regardless of case
        assert set(data1["results"]) == set(data2["results"])
    
    def test_search_partial_match(self):
        """Test that partial matches work"""
        response = client.get("/api/indian/stocks/search?query=TATA")
        assert response.status_code == 200
        
        data = response.json()
        # Should match multiple TATA companies
        assert len(data["results"]) > 1
        
        # Verify all results contain TATA
        for result in data["results"]:
            assert "TATA" in result.upper(), f"{result} should contain TATA"
    
    def test_search_returns_deduplicated_results(self):
        """Test that search results are de-duplicated"""
        response = client.get("/api/indian/stocks/search?query=RELIANCE")
        assert response.status_code == 200
        
        data = response.json()
        results = data["results"]
        
        # Check for no duplicates
        assert len(results) == len(set(results)), "Results should not contain duplicates"
    
    def test_search_response_structure(self):
        """Test that search response has correct structure"""
        response = client.get("/api/indian/stocks/search?query=INFY")
        assert response.status_code == 200
        
        data = response.json()
        
        # Verify response structure
        assert isinstance(data, dict)
        assert "query" in data
        assert "results" in data
        assert "total" in data
        assert "timestamp" in data
        
        assert isinstance(data["query"], str)
        assert isinstance(data["results"], list)
        assert isinstance(data["total"], int)
        assert isinstance(data["timestamp"], str)
        
        # Verify timestamp is valid ISO format
        try:
            datetime.fromisoformat(data["timestamp"])
        except ValueError:
            pytest.fail("timestamp should be valid ISO 8601 format")
    
    def test_search_no_results_returns_empty_list(self):
        """Test that search with no matches returns empty list"""
        response = client.get("/api/indian/stocks/search?query=ZZZZZZZZZ")
        assert response.status_code == 200
        
        data = response.json()
        assert data["results"] == []
        assert data["total"] == 0
    
    def test_search_query_preserved_in_response(self):
        """Test that the original query is preserved in response"""
        query = "Test Query"
        response = client.get(f"/api/indian/stocks/search?query={query}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["query"] == query
    
    def test_list_endpoint_unchanged(self):
        """Test that the existing list endpoint still works"""
        response = client.get("/api/indian/stocks/list")
        assert response.status_code == 200
        
        data = response.json()
        assert "stocks" in data
        assert "total" in data
        assert "timestamp" in data
        assert isinstance(data["stocks"], list)
        assert len(data["stocks"]) > 0
        assert data["total"] == len(data["stocks"])
