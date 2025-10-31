"""
Tests for timeframe mapper service
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.timeframe_mapper import TimeframeMapper, timeframe_mapper


class TestTimeframeMapper:
    """Test cases for TimeframeMapper"""
    
    def test_map_timeframe_1m(self):
        """Test mapping for 1m timeframe"""
        period, interval = TimeframeMapper.map_timeframe('1m')
        assert period == '7d'
        assert interval == '1m'
    
    def test_map_timeframe_3m(self):
        """Test mapping for 3m timeframe"""
        period, interval = TimeframeMapper.map_timeframe('3m')
        assert period == '7d'
        assert interval == '3m'
    
    def test_map_timeframe_5m(self):
        """Test mapping for 5m timeframe"""
        period, interval = TimeframeMapper.map_timeframe('5m')
        assert period == '30d'
        assert interval == '5m'
    
    def test_map_timeframe_15m(self):
        """Test mapping for 15m timeframe"""
        period, interval = TimeframeMapper.map_timeframe('15m')
        assert period == '60d'
        assert interval == '15m'
    
    def test_map_timeframe_30m(self):
        """Test mapping for 30m timeframe"""
        period, interval = TimeframeMapper.map_timeframe('30m')
        assert period == '120d'
        assert interval == '30m'
    
    def test_map_timeframe_1h(self):
        """Test mapping for 1h timeframe"""
        period, interval = TimeframeMapper.map_timeframe('1h')
        assert period == '2y'
        assert interval == '60m'
    
    def test_map_timeframe_4h(self):
        """Test mapping for 4h timeframe"""
        period, interval = TimeframeMapper.map_timeframe('4h')
        assert period == '5y'
        assert interval == '4h'
    
    def test_map_timeframe_1d(self):
        """Test mapping for 1d timeframe"""
        period, interval = TimeframeMapper.map_timeframe('1d')
        assert period == '5y'
        assert interval == '1d'
    
    def test_map_timeframe_1w(self):
        """Test mapping for 1w timeframe"""
        period, interval = TimeframeMapper.map_timeframe('1w')
        assert period == 'max'
        assert interval == '1wk'
    
    def test_map_timeframe_1mo(self):
        """Test mapping for 1mo timeframe"""
        period, interval = TimeframeMapper.map_timeframe('1mo')
        assert period == 'max'
        assert interval == '1mo'
    
    def test_map_timeframe_case_insensitive(self):
        """Test that mapping is case-insensitive"""
        period1, interval1 = TimeframeMapper.map_timeframe('1D')
        period2, interval2 = TimeframeMapper.map_timeframe('1d')
        assert period1 == period2
        assert interval1 == interval2
    
    def test_map_timeframe_invalid(self):
        """Test that invalid timeframe raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            TimeframeMapper.map_timeframe('2h')
        assert 'Invalid timeframe' in str(exc_info.value)
        assert '2h' in str(exc_info.value)
    
    def test_map_timeframe_empty(self):
        """Test that empty timeframe raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            TimeframeMapper.map_timeframe('')
        assert 'Timeframe cannot be empty' in str(exc_info.value)
    
    def test_map_timeframe_none(self):
        """Test that None timeframe raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            TimeframeMapper.map_timeframe(None)
        assert 'Timeframe cannot be empty' in str(exc_info.value)
    
    def test_validate_timeframe_valid(self):
        """Test validation of valid timeframes"""
        assert TimeframeMapper.validate_timeframe('1m') is True
        assert TimeframeMapper.validate_timeframe('1h') is True
        assert TimeframeMapper.validate_timeframe('1d') is True
        assert TimeframeMapper.validate_timeframe('1w') is True
        assert TimeframeMapper.validate_timeframe('1mo') is True
    
    def test_validate_timeframe_invalid(self):
        """Test validation of invalid timeframes"""
        assert TimeframeMapper.validate_timeframe('2h') is False
        assert TimeframeMapper.validate_timeframe('invalid') is False
        assert TimeframeMapper.validate_timeframe('') is False
        assert TimeframeMapper.validate_timeframe(None) is False
    
    def test_validate_timeframe_case_insensitive(self):
        """Test that validation is case-insensitive"""
        assert TimeframeMapper.validate_timeframe('1D') is True
        assert TimeframeMapper.validate_timeframe('1W') is True
        assert TimeframeMapper.validate_timeframe('1MO') is True
    
    def test_all_allowed_timeframes_in_map(self):
        """Test that all allowed timeframes have mappings"""
        for tf in TimeframeMapper.ALLOWED_TIMEFRAMES:
            assert tf in TimeframeMapper.TIMEFRAME_MAP
            mapping = TimeframeMapper.TIMEFRAME_MAP[tf]
            assert 'period' in mapping
            assert 'interval' in mapping
    
    def test_singleton_instance(self):
        """Test that timeframe_mapper is accessible"""
        assert timeframe_mapper is not None
        assert isinstance(timeframe_mapper, TimeframeMapper)
