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


class TestIndianSearchAPI:
    """Test cases for Indian stocks search endpoint"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.client = TestClient(app)
    
    def test_search_endpoint_exists(self):
        """Test that search endpoint is accessible"""
        response = self.client.get("/api/indian/stocks/search?query=TCS")
        assert response.status_code in [200, 503]  # 503 if service not available
    
    def test_search_hdfc_returns_hdfc_symbols(self):
        """Test that searching for HDFC returns HDFC-related symbols"""
        response = self.client.get("/api/indian/stocks/search?query=HDFC")
        
        if response.status_code == 503:
            pytest.skip("Indian stock service not available")
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        assert "query" in data
        assert "results" in data
        assert "total" in data
        assert "timestamp" in data
        
        assert data["query"] == "HDFC"
        assert isinstance(data["results"], list)
        assert data["total"] == len(data["results"])
        
        # Should return at least one of the HDFC symbols
        hdfc_symbols = ["HDFC", "HDFCBANK", "HDFCLIFE", "HDFCAMC"]
        found_symbols = [s for s in hdfc_symbols if s in data["results"]]
        assert len(found_symbols) > 0, f"Expected at least one of {hdfc_symbols} in results: {data['results']}"
    
    def test_search_tcs_ns_returns_tcs(self):
        """Test that searching for TCS.NS returns TCS"""
        response = self.client.get("/api/indian/stocks/search?query=TCS.NS")
        
        if response.status_code == 503:
            pytest.skip("Indian stock service not available")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["query"] == "TCS.NS"
        assert "TCS" in data["results"]
    
    def test_search_case_insensitive(self):
        """Test that search is case insensitive"""
        response_upper = self.client.get("/api/indian/stocks/search?query=RELIANCE")
        response_lower = self.client.get("/api/indian/stocks/search?query=reliance")
        response_mixed = self.client.get("/api/indian/stocks/search?query=Reliance")
        
        if response_upper.status_code == 503:
            pytest.skip("Indian stock service not available")
        
        assert response_upper.status_code == 200
        assert response_lower.status_code == 200
        assert response_mixed.status_code == 200
        
        # All should return the same results
        results_upper = set(response_upper.json()["results"])
        results_lower = set(response_lower.json()["results"])
        results_mixed = set(response_mixed.json()["results"])
        
        assert results_upper == results_lower == results_mixed
        assert "RELIANCE" in results_upper
    
    def test_search_partial_match(self):
        """Test that search supports partial matching"""
        response = self.client.get("/api/indian/stocks/search?query=ADANI")
        
        if response.status_code == 503:
            pytest.skip("Indian stock service not available")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return multiple ADANI symbols
        adani_symbols = [s for s in data["results"] if "ADANI" in s]
        assert len(adani_symbols) > 1, "Expected multiple ADANI symbols"
    
    def test_search_empty_query_validation(self):
        """Test that empty query returns 422 validation error"""
        # FastAPI Query validation with min_length=1 should return 422 for empty string
        response = self.client.get("/api/indian/stocks/search?query=")
        assert response.status_code == 422
    
    def test_search_missing_query_parameter(self):
        """Test that missing query parameter returns 422 validation error"""
        response = self.client.get("/api/indian/stocks/search")
        assert response.status_code == 422
    
    def test_search_query_too_long(self):
        """Test that query longer than 50 chars returns 422 validation error"""
        long_query = "A" * 51
        response = self.client.get(f"/api/indian/stocks/search?query={long_query}")
        assert response.status_code == 422
    
    def test_search_no_matches(self):
        """Test that search with no matches returns empty results"""
        response = self.client.get("/api/indian/stocks/search?query=ZZZZNONEXISTENT999")
        
        if response.status_code == 503:
            pytest.skip("Indian stock service not available")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["results"] == []
        assert data["total"] == 0
    
    def test_search_response_structure(self):
        """Test that search response has correct structure"""
        response = self.client.get("/api/indian/stocks/search?query=TCS")
        
        if response.status_code == 503:
            pytest.skip("Indian stock service not available")
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate all required fields are present
        assert "query" in data
        assert "results" in data
        assert "total" in data
        assert "timestamp" in data
        
        # Validate types
        assert isinstance(data["query"], str)
        assert isinstance(data["results"], list)
        assert isinstance(data["total"], int)
        assert isinstance(data["timestamp"], str)
        
        # Validate timestamp is ISO format
        from datetime import datetime
        datetime.fromisoformat(data["timestamp"])  # Should not raise
    
    def test_search_results_are_deduplicated(self):
        """Test that search results don't contain duplicates"""
        response = self.client.get("/api/indian/stocks/search?query=T")
        
        if response.status_code == 503:
            pytest.skip("Indian stock service not available")
        
        assert response.status_code == 200
        data = response.json()
        
        results = data["results"]
        # Check no duplicates
        assert len(results) == len(set(results)), "Results should not contain duplicates"
    
    def test_search_newly_added_symbols(self):
        """Test that search works for newly added NIFTY 500 symbols"""
        test_symbols = ["KOTAKBANK", "JSWSTEEL", "HCLTECH", "BRITANNIA", "TITAN"]
        
        for symbol in test_symbols:
            response = self.client.get(f"/api/indian/stocks/search?query={symbol}")
            
            if response.status_code == 503:
                pytest.skip("Indian stock service not available")
            
            assert response.status_code == 200
            data = response.json()
            assert symbol in data["results"], f"{symbol} should be found in search results"
    
    def test_list_endpoint_backward_compatible(self):
        """Test that the /api/indian/stocks/list endpoint still works as before"""
        response = self.client.get("/api/indian/stocks/list")
        
        if response.status_code == 503:
            pytest.skip("Indian stock service not available")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should have the expected structure
        assert "stocks" in data
        assert "total" in data
        assert "timestamp" in data
        
        # Should return a list of symbols
        assert isinstance(data["stocks"], list)
        assert data["total"] == len(data["stocks"])
        
        # Should contain more symbols than before (expanded coverage)
        assert data["total"] >= 50
