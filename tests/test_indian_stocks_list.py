"""
Tests for Indian stocks list mapping
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.indian_stock_service import IndianStockService


class TestIndianStocksList:
    """Test cases for Indian stocks list and mapping"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.service = IndianStockService()
    
    def test_service_initialization(self):
        """Test that service initializes properly"""
        assert self.service is not None
        assert isinstance(self.service.indian_stocks, dict)
        assert len(self.service.indian_stocks) > 0
    
    def test_expanded_mapping_contains_new_symbols(self):
        """Test that expanded mapping contains representative newly added symbols"""
        # Representative symbols from NIFTY 500 that should be in expanded mapping
        expected_symbols = [
            "KOTAKBANK",
            "JSWSTEEL",
            "HCLTECH",
            "TECHM",
            "BRITANNIA",
            "ADANIPORTS",
            "AMBUJACEM",
            "EICHERMOT",
            "HDFCLIFE",
            "SBICARD",
            "IOC",
            "BPCL",
            "GAIL",
            "HINDALCO",
            "ADANIGREEN",
            "ADANITRANS",
            "TITAN",
            "PAGEIND",
            "IRCTC",
        ]
        
        for symbol in expected_symbols:
            assert symbol in self.service.indian_stocks, f"{symbol} should be in expanded mapping"
    
    def test_all_symbols_have_ns_suffix(self):
        """Test that all ticker values end with .NS suffix"""
        for symbol, ticker in self.service.indian_stocks.items():
            assert ticker.endswith('.NS'), f"{symbol} -> {ticker} should end with .NS"
    
    def test_symbols_are_uppercase(self):
        """Test that all symbol keys are uppercase"""
        for symbol in self.service.indian_stocks.keys():
            assert symbol == symbol.upper(), f"Symbol {symbol} should be uppercase"
    
    def test_basic_symbols_still_present(self):
        """Test that basic symbols from original mapping are still present"""
        basic_symbols = [
            "RELIANCE",
            "TCS",
            "INFY",
            "WIPRO",
            "HDFCBANK",
            "ICICIBANK",
        ]
        
        for symbol in basic_symbols:
            assert symbol in self.service.indian_stocks, f"Basic symbol {symbol} should still be present"
    
    def test_mapping_has_expected_size(self):
        """Test that mapping has grown significantly (should be > 100 symbols)"""
        assert len(self.service.indian_stocks) > 100, "Expanded mapping should contain more than 100 symbols"
    
    def test_get_nse_symbol(self):
        """Test get_nse_symbol method works correctly"""
        # Test with known symbols
        assert self.service.get_nse_symbol("RELIANCE") == "RELIANCE.NS"
        assert self.service.get_nse_symbol("TCS") == "TCS.NS"
        assert self.service.get_nse_symbol("HDFCBANK") == "HDFCBANK.NS"
        
        # Test case insensitivity
        assert self.service.get_nse_symbol("reliance") == "RELIANCE.NS"
        
        # Test with .NS already present
        assert self.service.get_nse_symbol("RELIANCE.NS") == "RELIANCE.NS"
    
    def test_special_characters_in_symbols(self):
        """Test that symbols with special characters are handled"""
        # M&M should be in the mapping
        if "M&M" in self.service.indian_stocks:
            assert self.service.indian_stocks["M&M"].endswith('.NS')
    
    def test_alias_mappings(self):
        """Test that alias mappings work (e.g., ULTRATECH -> ULTRACEMCO.NS)"""
        # ULTRATECH should map to ULTRACEMCO.NS if present
        if "ULTRATECH" in self.service.indian_stocks:
            assert self.service.indian_stocks["ULTRATECH"] == "ULTRACEMCO.NS"
