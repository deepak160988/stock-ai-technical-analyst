"""
Tests for Indian stocks list - verify representative symbols are present
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.indian_stock_service import IndianStockService


class TestIndianStocksList:
    """Test cases for Indian stocks list"""
    
    # Representative symbols that should be present for NIFTY 500 coverage
    REQUIRED_SYMBOLS = [
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
    
    # Threshold for partial presence (allow some flexibility)
    PRESENCE_THRESHOLD = 0.7  # At least 70% of symbols should be present
    
    @pytest.fixture
    def indian_stock_service(self):
        """Create IndianStockService instance"""
        return IndianStockService()
    
    def test_representative_symbols_present(self, indian_stock_service):
        """Test that representative symbols are present in the mapping"""
        stocks = indian_stock_service.indian_stocks
        present_count = 0
        missing_symbols = []
        
        for symbol in self.REQUIRED_SYMBOLS:
            if symbol in stocks:
                present_count += 1
            else:
                missing_symbols.append(symbol)
        
        presence_ratio = present_count / len(self.REQUIRED_SYMBOLS)
        
        # Assert that at least PRESENCE_THRESHOLD of symbols are present
        assert presence_ratio >= self.PRESENCE_THRESHOLD, \
            f"Only {present_count}/{len(self.REQUIRED_SYMBOLS)} symbols present. Missing: {missing_symbols}"
    
    def test_symbols_have_valid_tickers(self, indian_stock_service):
        """Test that all symbols have valid NSE/BSE tickers"""
        stocks = indian_stock_service.indian_stocks
        
        for symbol, ticker in stocks.items():
            # All tickers should end with .NS or .BO
            assert ticker.endswith(".NS") or ticker.endswith(".BO"), \
                f"Symbol {symbol} has invalid ticker {ticker}"
    
    def test_symbols_are_uppercase(self, indian_stock_service):
        """Test that all symbol keys are uppercase"""
        stocks = indian_stock_service.indian_stocks
        
        for symbol in stocks.keys():
            assert symbol == symbol.upper(), \
                f"Symbol {symbol} is not uppercase"
    
    def test_minimum_coverage(self, indian_stock_service):
        """Test that we have broad coverage (at least 100 symbols)"""
        stocks = indian_stock_service.indian_stocks
        
        # Should have at least 100 symbols for NIFTY 500 coverage
        assert len(stocks) >= 100, \
            f"Expected at least 100 symbols, got {len(stocks)}"
    
    def test_json_mapping_loaded(self, indian_stock_service):
        """Test that JSON mapping was loaded (more symbols than in-code)"""
        # The in-code mapping has ~53 symbols
        # After loading JSON, we should have significantly more
        stocks = indian_stock_service.indian_stocks
        
        assert len(stocks) > 53, \
            f"Expected more than 53 symbols (in-code fallback), got {len(stocks)}"
