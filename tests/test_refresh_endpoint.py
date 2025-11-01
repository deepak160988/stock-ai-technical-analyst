"""
Tests for Indian Stock refresh endpoint
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app


class TestIndianStockRefreshEndpoint:
    """Test cases for POST /api/indian/stocks/refresh endpoint"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    @pytest.fixture
    def mock_success_result(self):
        """Mock successful refresh result"""
        return {
            "updated": True,
            "total": 500,
            "saved_cache": True,
            "saved_config": False,
            "source": "nse_csv",
            "timestamp": "2025-11-01T12:34:56Z",
            "errors": []
        }
    
    @pytest.fixture
    def mock_failure_result(self):
        """Mock failed refresh result"""
        return {
            "updated": False,
            "total": 10,
            "saved_cache": False,
            "saved_config": False,
            "source": "nse_csv",
            "timestamp": "2025-11-01T12:34:56Z",
            "errors": ["Failed to fetch from URL1", "Failed to fetch from URL2"]
        }
    
    def test_refresh_endpoint_success(self, client, mock_success_result):
        """Test successful refresh via endpoint"""
        with patch('main.indian_stock_service') as mock_service:
            mock_service.refresh_universe.return_value = mock_success_result
            
            response = client.post("/api/indian/stocks/refresh")
            
            assert response.status_code == 200
            data = response.json()
            
            assert data["updated"] is True
            assert data["total"] == 500
            assert data["saved_cache"] is True
            assert data["saved_config"] is False
            assert data["source"] == "nse_csv"
            assert "timestamp" in data
            
            # Verify service was called with correct parameters
            mock_service.refresh_universe.assert_called_once_with(save_to_config=False)
    
    def test_refresh_endpoint_with_save_to_config(self, client, mock_success_result):
        """Test refresh with save_to_config=true"""
        mock_success_result["saved_config"] = True
        
        with patch('main.indian_stock_service') as mock_service:
            mock_service.refresh_universe.return_value = mock_success_result
            
            response = client.post("/api/indian/stocks/refresh?save_to_config=true")
            
            assert response.status_code == 200
            data = response.json()
            
            assert data["updated"] is True
            assert data["saved_config"] is True
            
            # Verify service was called with save_to_config=True
            mock_service.refresh_universe.assert_called_once_with(save_to_config=True)
    
    def test_refresh_endpoint_failure(self, client, mock_failure_result):
        """Test refresh endpoint when refresh fails"""
        with patch('main.indian_stock_service') as mock_service:
            mock_service.refresh_universe.return_value = mock_failure_result
            
            response = client.post("/api/indian/stocks/refresh")
            
            assert response.status_code == 502
            data = response.json()
            
            assert "detail" in data
            assert "errors" in data["detail"]
    
    def test_refresh_endpoint_service_unavailable(self, client):
        """Test refresh endpoint when service is None"""
        with patch('main.indian_stock_service', None):
            response = client.post("/api/indian/stocks/refresh")
            
            assert response.status_code == 503
            data = response.json()
            assert "detail" in data
    
    def test_refresh_endpoint_exception(self, client):
        """Test refresh endpoint when service raises exception"""
        with patch('main.indian_stock_service') as mock_service:
            mock_service.refresh_universe.side_effect = Exception("Unexpected error")
            
            response = client.post("/api/indian/stocks/refresh")
            
            assert response.status_code == 500
            data = response.json()
            assert "detail" in data
