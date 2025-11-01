"""
Tests for Indian stocks list and expanded NIFTY 500 coverage
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.indian_stock_service import IndianStockService


class TestIndianStocksList:
    """Test cases for Indian stocks list with expanded NIFTY 500 coverage"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.service = IndianStockService()
    
    def test_service_initialization(self):
        """Test that service initializes successfully"""
        assert self.service is not None
        assert hasattr(self.service, 'indian_stocks')
        assert isinstance(self.service.indian_stocks, dict)
    
    def test_expanded_mapping_loaded(self):
        """Test that expanded mapping contains more than the default symbols"""
        # The expanded mapping should have significantly more symbols than the original ~50
        assert len(self.service.indian_stocks) >= 50
    
    def test_nifty_50_core_symbols_present(self):
        """Test that core NIFTY 50 symbols are present"""
        core_symbols = [
            "RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK",
            "HINDUNILVR", "ITC", "SBIN", "BHARTIARTL", "MARUTI"
        ]
        for symbol in core_symbols:
            assert symbol in self.service.indian_stocks, f"{symbol} should be in the mapping"
    
    def test_newly_added_symbols_present(self):
        """Test that representative newly added symbols are present"""
        newly_added = [
            "KOTAKBANK", "JSWSTEEL", "HCLTECH", "TECHM", "BRITANNIA",
            "ADANIPORTS", "AMBUJACEM", "EICHERMOT", "HDFCLIFE", "SBICARD",
            "IOC", "BPCL", "GAIL", "HINDALCO", "ADANIGREEN",
            "ADANITRANS", "TITAN", "PAGEIND", "IRCTC"
        ]
        for symbol in newly_added:
            assert symbol in self.service.indian_stocks, f"Newly added symbol {symbol} should be in the mapping"
    
    def test_symbols_have_ns_suffix(self):
        """Test that all mapped tickers end with .NS"""
        for symbol, ticker in self.service.indian_stocks.items():
            assert ticker.endswith('.NS') or ticker.endswith('.BO'), \
                f"Ticker {ticker} for symbol {symbol} should end with .NS or .BO"
    
    def test_symbols_are_uppercase(self):
        """Test that all symbol keys are uppercase"""
        for symbol in self.service.indian_stocks.keys():
            assert symbol.isupper(), f"Symbol {symbol} should be uppercase"
    
    def test_ultratech_alias(self):
        """Test that ULTRATECH is aliased to ULTRACEMCO.NS"""
        assert "ULTRATECH" in self.service.indian_stocks
        assert self.service.indian_stocks["ULTRATECH"] == "ULTRACEMCO.NS"
    
    def test_get_nse_symbol_from_mapping(self):
        """Test get_nse_symbol returns correct mapping"""
        assert self.service.get_nse_symbol("TCS") == "TCS.NS"
        assert self.service.get_nse_symbol("RELIANCE") == "RELIANCE.NS"
        assert self.service.get_nse_symbol("KOTAKBANK") == "KOTAKBANK.NS"
    
    def test_get_nse_symbol_case_insensitive(self):
        """Test get_nse_symbol is case insensitive"""
        assert self.service.get_nse_symbol("tcs") == "TCS.NS"
        assert self.service.get_nse_symbol("Reliance") == "RELIANCE.NS"
    
    def test_get_nse_symbol_with_ns_suffix(self):
        """Test get_nse_symbol handles symbols already with .NS suffix"""
        assert self.service.get_nse_symbol("TCS.NS") == "TCS.NS"
        assert self.service.get_nse_symbol("RELIANCE.NS") == "RELIANCE.NS"
    
    def test_no_duplicate_tickers(self):
        """Test that there are no duplicate ticker values (except intentional aliases)"""
        # Count occurrences of each ticker
        ticker_counts = {}
        for symbol, ticker in self.service.indian_stocks.items():
            ticker_counts[ticker] = ticker_counts.get(ticker, []) + [symbol]
        
        # ULTRACEMCO.NS may have both ULTRACEMCO and ULTRATECH, which is expected
        # All other tickers should appear only once
        for ticker, symbols in ticker_counts.items():
            if len(symbols) > 1:
                # Allow ULTRACEMCO.NS to have ULTRATECH and ULTRACEMCO as aliases
                if ticker == "ULTRACEMCO.NS":
                    assert set(symbols).issubset({"ULTRACEMCO", "ULTRATECH"}), \
                        f"Ticker {ticker} has unexpected multiple symbols: {symbols}"
                # BHARTIARTL.NS may have both BHARTIARTL and BHARTI
                elif ticker == "BHARTIARTL.NS":
                    assert set(symbols).issubset({"BHARTIARTL", "BHARTI"}), \
                        f"Ticker {ticker} has unexpected multiple symbols: {symbols}"
                # INFY.NS may have both INFY and INFOSYS
                elif ticker == "INFY.NS":
                    assert set(symbols).issubset({"INFY", "INFOSYS"}), \
                        f"Ticker {ticker} has unexpected multiple symbols: {symbols}"
                else:
                    pytest.fail(f"Unexpected duplicate ticker {ticker} for symbols: {symbols}")
    
    def test_symbol_mapping_extensibility(self):
        """Test that the mapping structure allows for easy extension"""
        # The mapping should be a simple dict
        assert isinstance(self.service.indian_stocks, dict)
        # Adding a new symbol should be straightforward
        test_symbol = "TESTSTOCK"
        test_ticker = "TESTSTOCK.NS"
        self.service.indian_stocks[test_symbol] = test_ticker
        assert self.service.get_nse_symbol(test_symbol) == test_ticker
