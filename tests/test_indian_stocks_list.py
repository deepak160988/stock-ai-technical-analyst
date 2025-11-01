"""
Tests for Indian stocks list - verifies representative symbols are present
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.indian_stock_service import indian_stock_service


class TestIndianStocksList:
    """Test cases for Indian stocks list"""
    
    def test_representative_symbols_present(self):
        """Test that representative NIFTY symbols are present"""
        # Define representative symbols that should be present
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
        
        # Get all symbols from the service
        all_symbols = set(indian_stock_service.indian_stocks.keys())
        
        # Count how many expected symbols are present
        present_symbols = [sym for sym in expected_symbols if sym in all_symbols]
        
        # Use a threshold to allow for some flexibility (e.g., 80% of symbols must be present)
        threshold = 0.8
        required_count = int(len(expected_symbols) * threshold)
        
        assert len(present_symbols) >= required_count, (
            f"Only {len(present_symbols)}/{len(expected_symbols)} representative symbols found. "
            f"Missing: {set(expected_symbols) - set(present_symbols)}"
        )
    
    def test_minimum_symbol_count(self):
        """Test that we have a reasonable number of symbols loaded"""
        symbols = indian_stock_service.indian_stocks
        # We should have at least 100 symbols (well below NIFTY 500, but a reasonable baseline)
        assert len(symbols) >= 100, f"Expected at least 100 symbols, got {len(symbols)}"
    
    def test_all_symbols_uppercase(self):
        """Test that all symbol keys are uppercase"""
        for symbol in indian_stock_service.indian_stocks.keys():
            assert symbol == symbol.upper(), f"Symbol {symbol} is not uppercase"
    
    def test_all_tickers_valid_format(self):
        """Test that all ticker values end with .NS or .BO"""
        for symbol, ticker in indian_stock_service.indian_stocks.items():
            assert ticker.endswith('.NS') or ticker.endswith('.BO'), (
                f"Ticker {ticker} for {symbol} doesn't end with .NS or .BO"
            )
