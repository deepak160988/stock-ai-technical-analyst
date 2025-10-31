"""
Timeframe mapper utility for converting user-friendly timeframe strings
to yfinance-compatible period and interval parameters.
"""
from typing import Dict, List


# Valid timeframes that users can select
VALID_TIMEFRAMES: List[str] = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '5y', 'max']


def map_timeframe(timeframe: str) -> Dict[str, str]:
    """
    Map a user-friendly timeframe string to yfinance period and interval parameters.
    
    Args:
        timeframe: User-selected timeframe (e.g., '1d', '1mo', '1y')
        
    Returns:
        Dictionary with 'period' and 'interval' keys
        
    Raises:
        ValueError: If timeframe is not valid
        
    Examples:
        >>> map_timeframe('1d')
        {'period': '1d', 'interval': '5m'}
        >>> map_timeframe('1mo')
        {'period': '1mo', 'interval': '1h'}
    """
    if not timeframe or not isinstance(timeframe, str):
        raise ValueError(f"Timeframe must be a non-empty string, got: {timeframe}")
    
    timeframe = timeframe.lower().strip()
    
    # Mapping of timeframes to yfinance parameters
    # Short timeframes use smaller intervals for better granularity
    # Longer timeframes use larger intervals to reduce data size
    timeframe_map = {
        '1d': {'period': '1d', 'interval': '5m'},     # Intraday: 5-minute intervals
        '5d': {'period': '5d', 'interval': '15m'},    # 5 days: 15-minute intervals
        '1mo': {'period': '1mo', 'interval': '1h'},   # 1 month: hourly intervals
        '3mo': {'period': '3mo', 'interval': '1d'},   # 3 months: daily intervals
        '6mo': {'period': '6mo', 'interval': '1d'},   # 6 months: daily intervals
        '1y': {'period': '1y', 'interval': '1d'},     # 1 year: daily intervals
        '5y': {'period': '5y', 'interval': '1d'},     # 5 years: daily intervals
        'max': {'period': 'max', 'interval': '1d'},   # Maximum available: daily intervals
    }
    
    if timeframe not in timeframe_map:
        raise ValueError(
            f"Invalid timeframe '{timeframe}'. Must be one of: {', '.join(VALID_TIMEFRAMES)}"
        )
    
    return timeframe_map[timeframe]


def get_valid_timeframes() -> List[str]:
    """
    Get the list of valid timeframe values.
    
    Returns:
        List of valid timeframe strings
    """
    return VALID_TIMEFRAMES.copy()
