"""
Tests for Indian stocks list and expanded symbol mapping
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.indian_stock_service import IndianStockService


class TestIndianStocksList:
    """Test cases for Indian stocks expanded mapping"""
    
    def setup_method(self):
        """Setup test instance"""
        self.service = IndianStockService()
    
    def test_service_initialization(self):
        """Test that service initializes properly"""
        assert self.service is not None
        assert isinstance(self.service.indian_stocks, dict)
        assert len(self.service.indian_stocks) > 0
    
    def test_basic_symbols_present(self):
        """Test that basic NIFTY 50 symbols are present"""
        basic_symbols = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "SBIN"]
        for symbol in basic_symbols:
            assert symbol in self.service.indian_stocks
            assert self.service.indian_stocks[symbol].endswith(".NS")
    
    def test_newly_added_symbols_present(self):
        """Test that newly added symbols from expanded mapping are present"""
        newly_added = [
            "KOTAKBANK",    # Private bank
            "JSWSTEEL",     # Steel
            "HCLTECH",      # IT
            "TECHM",        # IT
            "BRITANNIA",    # FMCG
            "ADANIPORTS",   # Infrastructure
            "AMBUJACEM",    # Cement
            "EICHERMOT",    # Auto
            "HDFCLIFE",     # Insurance
            "SBICARD",      # Financial services
            "IOC",          # Oil & Gas
            "BPCL",         # Oil & Gas
            "GAIL",         # Oil & Gas
            "HINDALCO",     # Metals
            "ADANIGREEN",   # Energy
            "ADANITRANS",   # Infrastructure
            "TITAN",        # Consumer
            "PAGEIND",      # FMCG
            "IRCTC"         # Travel
        ]
        
        for symbol in newly_added:
            assert symbol in self.service.indian_stocks, f"Symbol {symbol} should be in expanded mapping"
            assert self.service.indian_stocks[symbol].endswith(".NS"), f"Symbol {symbol} should have .NS suffix"
    
    def test_symbol_count_expansion(self):
        """Test that we have significantly more symbols than the original hardcoded list"""
        # Original hardcoded list had about 45 symbols
        # Expanded list should have at least 200+ symbols (targeting ~500)
        assert len(self.service.indian_stocks) >= 200, \
            f"Expected at least 200 symbols, got {len(self.service.indian_stocks)}"
    
    def test_nse_suffix(self):
        """Test that all symbols have .NS suffix"""
        for symbol, ticker in self.service.indian_stocks.items():
            assert ticker.endswith(".NS") or ticker.endswith(".BO"), \
                f"Ticker {ticker} for {symbol} should end with .NS or .BO"
    
    def test_symbol_uppercase(self):
        """Test that all symbol keys are uppercase"""
        for symbol in self.service.indian_stocks.keys():
            assert symbol.isupper(), f"Symbol {symbol} should be uppercase"
    
    def test_get_nse_symbol(self):
        """Test get_nse_symbol method with expanded mapping"""
        # Test known symbols
        assert self.service.get_nse_symbol("RELIANCE") == "RELIANCE.NS"
        assert self.service.get_nse_symbol("KOTAKBANK") == "KOTAKBANK.NS"
        assert self.service.get_nse_symbol("HDFCLIFE") == "HDFCLIFE.NS"
        
        # Test case insensitivity
        assert self.service.get_nse_symbol("reliance") == "RELIANCE.NS"
        assert self.service.get_nse_symbol("kotakbank") == "KOTAKBANK.NS"
    
    def test_validate_indian_symbol(self):
        """Test symbol validation (without network requests)"""
        # Basic validation should pass for any non-empty string
        assert self.service.validate_indian_symbol("RELIANCE") == True
        assert self.service.validate_indian_symbol("KOTAKBANK") == True
        assert self.service.validate_indian_symbol("XYZ") == True  # Lenient validation
    
    def test_ultratech_alias(self):
        """Test that ULTRATECH maps to ULTRACEMCO.NS"""
        if "ULTRATECH" in self.service.indian_stocks:
            assert self.service.indian_stocks["ULTRATECH"] == "ULTRACEMCO.NS"
    
    def test_financial_services_coverage(self):
        """Test coverage of financial services sector"""
        financial_symbols = [
            "HDFCBANK", "ICICIBANK", "KOTAKBANK", "AXISBANK", "SBIN",
            "HDFCLIFE", "SBICARD", "BAJFINANCE", "BAJAJFINSV"
        ]
        for symbol in financial_symbols:
            assert symbol in self.service.indian_stocks, \
                f"Financial symbol {symbol} should be present"
    
    def test_it_sector_coverage(self):
        """Test coverage of IT sector"""
        it_symbols = ["TCS", "INFY", "WIPRO", "HCLTECH", "TECHM"]
        for symbol in it_symbols:
            assert symbol in self.service.indian_stocks, \
                f"IT symbol {symbol} should be present"
    
    def test_energy_sector_coverage(self):
        """Test coverage of energy/oil & gas sector"""
        energy_symbols = ["RELIANCE", "IOC", "BPCL", "ONGC", "NTPC", "POWERGRID"]
        for symbol in energy_symbols:
            assert symbol in self.service.indian_stocks, \
                f"Energy symbol {symbol} should be present"
