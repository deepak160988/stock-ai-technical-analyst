"""
Tests for Indian stocks list coverage
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.indian_stock_service import IndianStockService


class TestIndianStocksList:
    """Test cases for Indian stocks list coverage"""
    
    def test_representative_symbols_present(self):
        """Test that representative NIFTY symbols are present"""
        service = IndianStockService()
        
        # Representative symbols that should be present
        representative_symbols = [
            "KOTAKBANK", "JSWSTEEL", "HCLTECH", "TECHM", "BRITANNIA",
            "ADANIPORTS", "AMBUJACEM", "EICHERMOT", "HDFCLIFE", "SBICARD",
            "IOC", "BPCL", "GAIL", "HINDALCO", "ADANIGREEN",
            "ADANITRANS", "TITAN", "PAGEIND", "IRCTC"
        ]
        
        present_count = 0
        missing_symbols = []
        
        for symbol in representative_symbols:
            if symbol in service.indian_stocks:
                present_count += 1
            else:
                missing_symbols.append(symbol)
        
        # Allow partial presence (at least 70% of representative symbols)
        threshold = len(representative_symbols) * 0.7
        
        assert present_count >= threshold, \
            f"Only {present_count}/{len(representative_symbols)} representative symbols present. " \
            f"Missing: {missing_symbols}"
    
    def test_total_symbols_count(self):
        """Test that we have significant coverage (at least 100 symbols)"""
        service = IndianStockService()
        total_symbols = len(service.indian_stocks)
        
        assert total_symbols >= 100, \
            f"Expected at least 100 symbols for broad coverage, got {total_symbols}"
    
    def test_all_tickers_valid_format(self):
        """Test that all tickers end with .NS or .BO"""
        service = IndianStockService()
        
        invalid_tickers = []
        for symbol, ticker in service.indian_stocks.items():
            if not (ticker.endswith('.NS') or ticker.endswith('.BO')):
                invalid_tickers.append((symbol, ticker))
        
        assert len(invalid_tickers) == 0, \
            f"Found invalid tickers (not ending with .NS or .BO): {invalid_tickers}"
    
    def test_all_keys_uppercase(self):
        """Test that all symbol keys are uppercase"""
        service = IndianStockService()
        
        non_uppercase = []
        for symbol in service.indian_stocks.keys():
            if symbol != symbol.upper():
                non_uppercase.append(symbol)
        
        assert len(non_uppercase) == 0, \
            f"Found non-uppercase symbol keys: {non_uppercase}"
    
    def test_json_loading(self):
        """Test that JSON file is loaded if present"""
        service = IndianStockService()
        
        # Check for specific symbols that are in the JSON but not in the minimal in-code mapping
        extended_symbols = ["KOTAKBANK", "JSWSTEEL", "HCLTECH"]
        
        found_count = 0
        for symbol in extended_symbols:
            if symbol in service.indian_stocks:
                found_count += 1
        
        # If any of these extended symbols are found, JSON loading worked
        assert found_count > 0, "JSON loading may not be working, extended symbols not found"
