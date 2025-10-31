#!/usr/bin/env python3
"""
Unit tests for timeframe mapping functionality
"""
import sys
import pytest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.stock_service import map_timeframe, ALLOWED_TIMEFRAMES, TIMEFRAME_MAPPING


class TestTimeframeMapping:
    """Test cases for timeframe mapping"""
    
    def test_valid_timeframes(self):
        """Test that all valid timeframes map correctly"""
        for timeframe in ALLOWED_TIMEFRAMES:
            result = map_timeframe(timeframe)
            assert 'period' in result
            assert 'interval' in result
            assert result == TIMEFRAME_MAPPING[timeframe]
    
    def test_1m_timeframe(self):
        """Test 1-minute timeframe mapping"""
        result = map_timeframe('1m')
        assert result['period'] == '7d'
        assert result['interval'] == '1m'
    
    def test_5m_timeframe(self):
        """Test 5-minute timeframe mapping"""
        result = map_timeframe('5m')
        assert result['period'] == '30d'
        assert result['interval'] == '5m'
    
    def test_1h_timeframe(self):
        """Test 1-hour timeframe mapping"""
        result = map_timeframe('1h')
        assert result['period'] == '2y'
        assert result['interval'] == '60m'
    
    def test_1d_timeframe(self):
        """Test 1-day timeframe mapping"""
        result = map_timeframe('1d')
        assert result['period'] == '5y'
        assert result['interval'] == '1d'
    
    def test_1w_timeframe(self):
        """Test 1-week timeframe mapping"""
        result = map_timeframe('1w')
        assert result['period'] == 'max'
        assert result['interval'] == '1wk'
    
    def test_1mo_timeframe(self):
        """Test 1-month timeframe mapping"""
        result = map_timeframe('1mo')
        assert result['period'] == 'max'
        assert result['interval'] == '1mo'
    
    def test_none_timeframe(self):
        """Test that None timeframe returns empty dict"""
        result = map_timeframe(None)
        assert result == {}
    
    def test_invalid_timeframe(self):
        """Test that invalid timeframe raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            map_timeframe('invalid')
        assert 'Invalid timeframe' in str(exc_info.value)
    
    def test_invalid_timeframe_with_valid_format(self):
        """Test that a timeframe with valid format but not in list raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            map_timeframe('2h')
        assert 'Invalid timeframe' in str(exc_info.value)
    
    def test_case_sensitivity(self):
        """Test that timeframe is case-sensitive"""
        with pytest.raises(ValueError):
            map_timeframe('1M')  # Should fail, must be lowercase
    
    def test_all_allowed_timeframes_have_mappings(self):
        """Test that all allowed timeframes have corresponding mappings"""
        for timeframe in ALLOWED_TIMEFRAMES:
            assert timeframe in TIMEFRAME_MAPPING
    
    def test_mapping_completeness(self):
        """Test that all mappings are in allowed list"""
        for timeframe in TIMEFRAME_MAPPING.keys():
            assert timeframe in ALLOWED_TIMEFRAMES


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
