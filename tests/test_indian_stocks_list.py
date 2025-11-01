"""
Tests for Indian stocks list expansion
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.indian_stock_service import IndianStockService


class TestIndianStocksList:
    """Test cases for expanded Indian stocks mapping"""

    def test_expanded_mapping_contains_new_symbols(self):
        """Test that the expanded mapping contains representative newly added symbols"""
        service = IndianStockService()
        
        # Representative symbols from expanded coverage
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
            assert symbol in service.indian_stocks, f"Expected symbol {symbol} not found in mapping"
            assert service.indian_stocks[symbol].endswith(".NS"), f"Symbol {symbol} should have .NS suffix"

    def test_original_symbols_still_present(self):
        """Test that original symbols are still present after expansion"""
        service = IndianStockService()
        
        # Original symbols from hardcoded mapping
        original_symbols = [
            "RELIANCE",
            "TCS",
            "INFY",
            "WIPRO",
            "HDFCBANK",
            "ICICIBANK",
        ]
        
        for symbol in original_symbols:
            assert symbol in service.indian_stocks, f"Original symbol {symbol} missing after expansion"

    def test_symbol_ticker_format(self):
        """Test that all tickers have proper .NS suffix"""
        service = IndianStockService()
        
        for symbol, ticker in service.indian_stocks.items():
            assert ticker.endswith(".NS") or ticker.endswith(".BO"), \
                f"Ticker {ticker} for symbol {symbol} should end with .NS or .BO"

    def test_expanded_coverage_count(self):
        """Test that we have significantly expanded coverage (at least 100 symbols for NIFTY 500 coverage)"""
        service = IndianStockService()
        
        # Should have at least 100 symbols for broad coverage
        assert len(service.indian_stocks) >= 100, \
            f"Expected at least 100 symbols for NIFTY 500 coverage, got {len(service.indian_stocks)}"

    def test_ultratech_alias(self):
        """Test that ULTRATECH alias points to ULTRACEMCO.NS"""
        service = IndianStockService()
        
        assert "ULTRATECH" in service.indian_stocks
        assert service.indian_stocks["ULTRATECH"] == "ULTRACEMCO.NS"

    def test_symbol_keys_uppercase(self):
        """Test that all symbol keys are uppercase"""
        service = IndianStockService()
        
        for symbol in service.indian_stocks.keys():
            assert symbol == symbol.upper(), f"Symbol {symbol} should be uppercase"
