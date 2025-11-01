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
    """Test cases for Indian stocks search API endpoint"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)
    
    def test_search_endpoint_exists(self):
        """Test that search endpoint is accessible"""
        response = self.client.get("/api/indian/stocks/search?query=TCS")
        assert response.status_code in [200, 503]  # 503 if service not available
    
    def test_search_hdfc_returns_matches(self):
        """Test that searching for HDFC returns relevant results"""
        response = self.client.get("/api/indian/stocks/search?query=HDFC")
        
        if response.status_code == 503:
            pytest.skip("Indian stock service not available")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "query" in data
        assert "results" in data
        assert "total" in data
        assert "timestamp" in data
        
        # Verify query is preserved
        assert data["query"] == "HDFC"
        
        # Verify we have results
        assert isinstance(data["results"], list)
        assert data["total"] == len(data["results"])
        
        # Verify at least one HDFC-related symbol is present
        hdfc_symbols = ["HDFC", "HDFCBANK", "HDFCLIFE", "HDFCAMC"]
        assert any(symbol in data["results"] for symbol in hdfc_symbols), \
            f"Expected at least one of {hdfc_symbols} in results, got {data['results']}"
    
    def test_search_tcs_ns_ticker(self):
        """Test searching by ticker with .NS suffix returns correct result"""
        response = self.client.get("/api/indian/stocks/search?query=TCS.NS")
        
        if response.status_code == 503:
            pytest.skip("Indian stock service not available")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return TCS
        assert "TCS" in data["results"]
    
    def test_search_case_insensitive(self):
        """Test that search is case-insensitive"""
        response_upper = self.client.get("/api/indian/stocks/search?query=RELIANCE")
        response_lower = self.client.get("/api/indian/stocks/search?query=reliance")
        
        if response_upper.status_code == 503:
            pytest.skip("Indian stock service not available")
        
        assert response_upper.status_code == 200
        assert response_lower.status_code == 200
        
        # Both should return same results
        assert response_upper.json()["results"] == response_lower.json()["results"]
    
    def test_search_partial_match(self):
        """Test that partial matches work"""
        response = self.client.get("/api/indian/stocks/search?query=ADANI")
        
        if response.status_code == 503:
            pytest.skip("Indian stock service not available")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return multiple Adani group stocks
        assert len(data["results"]) > 0
        
        # All results should contain "ADANI" in the symbol
        for symbol in data["results"]:
            assert "ADANI" in symbol.upper()
    
    def test_search_empty_query_validation(self):
        """Test that empty query returns 400 error"""
        # Test completely empty query
        response = self.client.get("/api/indian/stocks/search?query=")
        assert response.status_code == 422  # FastAPI validation error for empty string
        
        # Test whitespace-only query
        response = self.client.get("/api/indian/stocks/search?query=   ")
        if response.status_code == 200:
            # If it passes validation, ensure service handles it
            data = response.json()
            assert "results" in data
    
    def test_search_missing_query_param(self):
        """Test that missing query parameter returns error"""
        response = self.client.get("/api/indian/stocks/search")
        assert response.status_code == 422  # FastAPI validation error
    
    def test_search_query_length_validation(self):
        """Test query length validation (1-50 chars)"""
        # Valid length query
        response = self.client.get("/api/indian/stocks/search?query=TCS")
        assert response.status_code in [200, 503]
        
        # Query too long (>50 chars)
        long_query = "A" * 51
        response = self.client.get(f"/api/indian/stocks/search?query={long_query}")
        assert response.status_code == 422
    
    def test_search_returns_deduplicated_results(self):
        """Test that search results are deduplicated"""
        response = self.client.get("/api/indian/stocks/search?query=TATA")
        
        if response.status_code == 503:
            pytest.skip("Indian stock service not available")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check no duplicates
        results = data["results"]
        assert len(results) == len(set(results)), "Results should not contain duplicates"
    
    def test_search_response_format(self):
        """Test that search response has correct format"""
        response = self.client.get("/api/indian/stocks/search?query=INFY")
        
        if response.status_code == 503:
            pytest.skip("Indian stock service not available")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify all required fields
        required_fields = ["query", "results", "total", "timestamp"]
        for field in required_fields:
            assert field in data, f"Response should contain '{field}' field"
        
        # Verify data types
        assert isinstance(data["query"], str)
        assert isinstance(data["results"], list)
        assert isinstance(data["total"], int)
        assert isinstance(data["timestamp"], str)
        
        # Verify total matches results length
        assert data["total"] == len(data["results"])
    
    def test_search_it_stocks(self):
        """Test searching for IT sector stocks"""
        response = self.client.get("/api/indian/stocks/search?query=TECH")
        
        if response.status_code == 503:
            pytest.skip("Indian stock service not available")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should find TECHM and HCLTECH
        tech_symbols = [s for s in data["results"] if "TECH" in s]
        assert len(tech_symbols) > 0
    
    def test_search_banking_stocks(self):
        """Test searching for banking stocks"""
        response = self.client.get("/api/indian/stocks/search?query=BANK")
        
        if response.status_code == 503:
            pytest.skip("Indian stock service not available")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should find multiple banks
        assert len(data["results"]) > 0
        
        # Check for common bank symbols
        bank_symbols = ["HDFCBANK", "ICICIBANK", "AXISBANK", "KOTAKBANK", "SBIN"]
        found_banks = [s for s in data["results"] if s in bank_symbols]
        assert len(found_banks) > 0
    
    def test_list_endpoint_still_works(self):
        """Test that the existing list endpoint still works and returns expanded list"""
        response = self.client.get("/api/indian/stocks/list")
        
        if response.status_code == 503:
            pytest.skip("Indian stock service not available")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "stocks" in data
        assert "total" in data
        assert "timestamp" in data
        
        # Verify it has expanded coverage
        assert len(data["stocks"]) >= 200, \
            f"Expected at least 200 stocks in list, got {len(data['stocks'])}"
