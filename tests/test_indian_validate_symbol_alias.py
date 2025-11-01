"""
Tests for IndianStockService validate_symbol alias
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.indian_stock_service import IndianStockService, indian_stock_service


class TestIndianValidateSymbolAlias:
    """Test cases for validate_symbol alias in IndianStockService"""
    
    def test_validate_symbol_method_exists(self):
        """Test that validate_symbol method exists"""
        service = IndianStockService()
        assert hasattr(service, 'validate_symbol'), "validate_symbol method should exist"
        assert callable(service.validate_symbol), "validate_symbol should be callable"
    
    def test_validate_symbol_method_exists_on_singleton(self):
        """Test that validate_symbol method exists on singleton instance"""
        assert hasattr(indian_stock_service, 'validate_symbol'), "validate_symbol method should exist on singleton"
        assert callable(indian_stock_service.validate_symbol), "validate_symbol should be callable on singleton"
    
    def test_validate_symbol_returns_same_as_validate_indian_symbol_valid(self):
        """Test that validate_symbol returns same result as validate_indian_symbol for valid symbol"""
        service = IndianStockService()
        symbol = 'RELIANCE'
        
        result_indian = service.validate_indian_symbol(symbol)
        result_alias = service.validate_symbol(symbol)
        
        assert result_alias == result_indian, f"validate_symbol and validate_indian_symbol should return same result for {symbol}"
    
    def test_validate_symbol_returns_same_as_validate_indian_symbol_known_symbols(self):
        """Test that validate_symbol returns same result as validate_indian_symbol for multiple known symbols"""
        service = IndianStockService()
        test_symbols = ['RELIANCE', 'TCS', 'INFY', 'WIPRO', 'HDFCBANK']
        
        for symbol in test_symbols:
            result_indian = service.validate_indian_symbol(symbol)
            result_alias = service.validate_symbol(symbol)
            assert result_alias == result_indian, f"Results should match for {symbol}"
    
    def test_validate_symbol_returns_same_as_validate_indian_symbol_empty_string(self):
        """Test that validate_symbol returns same result as validate_indian_symbol for empty string"""
        service = IndianStockService()
        symbol = ''
        
        result_indian = service.validate_indian_symbol(symbol)
        result_alias = service.validate_symbol(symbol)
        
        assert result_alias == result_indian, "validate_symbol and validate_indian_symbol should return same result for empty string"
    
    def test_validate_symbol_returns_same_as_validate_indian_symbol_invalid_symbol(self):
        """Test that validate_symbol returns same result as validate_indian_symbol for invalid symbol"""
        service = IndianStockService()
        # Using a very long string that should be invalid
        symbol = 'THISISAVERYLONGINVALIDSYMBOL'
        
        result_indian = service.validate_indian_symbol(symbol)
        result_alias = service.validate_symbol(symbol)
        
        assert result_alias == result_indian, "validate_symbol and validate_indian_symbol should return same result for invalid symbol"
    
    def test_validate_symbol_returns_same_as_validate_indian_symbol_short_symbol(self):
        """Test that validate_symbol returns same result as validate_indian_symbol for short symbol"""
        service = IndianStockService()
        symbol = 'LT'
        
        result_indian = service.validate_indian_symbol(symbol)
        result_alias = service.validate_symbol(symbol)
        
        assert result_alias == result_indian, f"validate_symbol and validate_indian_symbol should return same result for {symbol}"
    
    def test_validate_symbol_returns_same_as_validate_indian_symbol_nse_format(self):
        """Test that validate_symbol returns same result as validate_indian_symbol for NSE format symbol"""
        service = IndianStockService()
        symbol = 'RELIANCE.NS'
        
        result_indian = service.validate_indian_symbol(symbol)
        result_alias = service.validate_symbol(symbol)
        
        assert result_alias == result_indian, "validate_symbol and validate_indian_symbol should return same result for NSE format"
    
    def test_validate_symbol_returns_same_as_validate_indian_symbol_bse_format(self):
        """Test that validate_symbol returns same result as validate_indian_symbol for BSE format symbol"""
        service = IndianStockService()
        symbol = 'RELIANCE.BO'
        
        result_indian = service.validate_indian_symbol(symbol)
        result_alias = service.validate_symbol(symbol)
        
        assert result_alias == result_indian, "validate_symbol and validate_indian_symbol should return same result for BSE format"
    
    def test_validate_symbol_returns_same_as_validate_indian_symbol_lowercase(self):
        """Test that validate_symbol returns same result as validate_indian_symbol for lowercase symbol"""
        service = IndianStockService()
        symbol = 'reliance'
        
        result_indian = service.validate_indian_symbol(symbol)
        result_alias = service.validate_symbol(symbol)
        
        assert result_alias == result_indian, "validate_symbol and validate_indian_symbol should return same result for lowercase"
    
    def test_validate_symbol_parity_with_stock_service(self):
        """Test that IndianStockService now has same validate_symbol method as StockService"""
        from services.stock_service import StockService
        
        indian_service = IndianStockService()
        stock_service = StockService()
        
        # Both should have validate_symbol method
        assert hasattr(indian_service, 'validate_symbol'), "IndianStockService should have validate_symbol"
        assert hasattr(stock_service, 'validate_symbol'), "StockService should have validate_symbol"
        
        # Both methods should be callable
        assert callable(indian_service.validate_symbol), "IndianStockService.validate_symbol should be callable"
        assert callable(stock_service.validate_symbol), "StockService.validate_symbol should be callable"
