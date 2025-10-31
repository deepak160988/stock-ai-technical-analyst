"""
Unit tests for timeframe_mapper module.
"""
import pytest
from utils.timeframe_mapper import map_timeframe, get_valid_timeframes, VALID_TIMEFRAMES


class TestMapTimeframe:
    """Tests for map_timeframe function"""
    
    def test_map_timeframe_1d(self):
        """Test mapping for 1 day timeframe"""
        result = map_timeframe('1d')
        assert result == {'period': '1d', 'interval': '5m'}
    
    def test_map_timeframe_5d(self):
        """Test mapping for 5 day timeframe"""
        result = map_timeframe('5d')
        assert result == {'period': '5d', 'interval': '15m'}
    
    def test_map_timeframe_1mo(self):
        """Test mapping for 1 month timeframe"""
        result = map_timeframe('1mo')
        assert result == {'period': '1mo', 'interval': '1h'}
    
    def test_map_timeframe_3mo(self):
        """Test mapping for 3 month timeframe"""
        result = map_timeframe('3mo')
        assert result == {'period': '3mo', 'interval': '1d'}
    
    def test_map_timeframe_6mo(self):
        """Test mapping for 6 month timeframe"""
        result = map_timeframe('6mo')
        assert result == {'period': '6mo', 'interval': '1d'}
    
    def test_map_timeframe_1y(self):
        """Test mapping for 1 year timeframe"""
        result = map_timeframe('1y')
        assert result == {'period': '1y', 'interval': '1d'}
    
    def test_map_timeframe_5y(self):
        """Test mapping for 5 year timeframe"""
        result = map_timeframe('5y')
        assert result == {'period': '5y', 'interval': '1d'}
    
    def test_map_timeframe_max(self):
        """Test mapping for max timeframe"""
        result = map_timeframe('max')
        assert result == {'period': 'max', 'interval': '1d'}
    
    def test_map_timeframe_case_insensitive(self):
        """Test that timeframe mapping is case insensitive"""
        result_lower = map_timeframe('1mo')
        result_upper = map_timeframe('1MO')
        result_mixed = map_timeframe('1Mo')
        assert result_lower == result_upper == result_mixed
    
    def test_map_timeframe_whitespace_handling(self):
        """Test that whitespace is handled correctly"""
        result = map_timeframe('  1mo  ')
        assert result == {'period': '1mo', 'interval': '1h'}
    
    def test_map_timeframe_invalid_raises_error(self):
        """Test that invalid timeframe raises ValueError"""
        with pytest.raises(ValueError, match="Invalid timeframe"):
            map_timeframe('invalid')
    
    def test_map_timeframe_empty_string_raises_error(self):
        """Test that empty string raises ValueError"""
        with pytest.raises(ValueError, match="Timeframe must be a non-empty string"):
            map_timeframe('')
    
    def test_map_timeframe_none_raises_error(self):
        """Test that None raises ValueError"""
        with pytest.raises(ValueError, match="Timeframe must be a non-empty string"):
            map_timeframe(None)
    
    def test_map_timeframe_non_string_raises_error(self):
        """Test that non-string input raises ValueError"""
        with pytest.raises(ValueError, match="Timeframe must be a non-empty string"):
            map_timeframe(123)
    
    def test_all_valid_timeframes_work(self):
        """Test that all valid timeframes map successfully"""
        for timeframe in VALID_TIMEFRAMES:
            result = map_timeframe(timeframe)
            assert 'period' in result
            assert 'interval' in result
            assert isinstance(result['period'], str)
            assert isinstance(result['interval'], str)


class TestGetValidTimeframes:
    """Tests for get_valid_timeframes function"""
    
    def test_get_valid_timeframes_returns_list(self):
        """Test that get_valid_timeframes returns a list"""
        result = get_valid_timeframes()
        assert isinstance(result, list)
    
    def test_get_valid_timeframes_not_empty(self):
        """Test that get_valid_timeframes returns non-empty list"""
        result = get_valid_timeframes()
        assert len(result) > 0
    
    def test_get_valid_timeframes_matches_constant(self):
        """Test that get_valid_timeframes matches VALID_TIMEFRAMES"""
        result = get_valid_timeframes()
        assert result == VALID_TIMEFRAMES
    
    def test_get_valid_timeframes_returns_copy(self):
        """Test that get_valid_timeframes returns a copy, not the original"""
        result = get_valid_timeframes()
        result.append('test')
        assert 'test' not in VALID_TIMEFRAMES
