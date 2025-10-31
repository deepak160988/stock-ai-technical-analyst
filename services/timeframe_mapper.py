"""
Timeframe mapping service for converting TradingView-style timeframes
to yfinance period and interval parameters.
"""

from typing import Dict, Tuple, List
import logging

logger = logging.getLogger(__name__)


class TimeframeMapper:
    """Maps timeframe values to yfinance period and interval parameters."""

    # Allowed timeframe values
    ALLOWED_TIMEFRAMES: List[str] = [
        "1m",
        "3m",
        "5m",
        "15m",
        "30m",
        "1h",
        "4h",
        "1d",
        "1w",
        "1mo",
    ]

    # Canonical mapping of timeframe to period and interval
    TIMEFRAME_MAP: Dict[str, Dict[str, str]] = {
        "1m": {"period": "7d", "interval": "1m"},
        "3m": {"period": "7d", "interval": "3m"},
        "5m": {"period": "30d", "interval": "5m"},
        "15m": {"period": "60d", "interval": "15m"},
        "30m": {"period": "120d", "interval": "30m"},
        "1h": {"period": "2y", "interval": "60m"},
        "4h": {"period": "5y", "interval": "4h"},
        "1d": {"period": "5y", "interval": "1d"},
        "1w": {"period": "max", "interval": "1wk"},
        "1mo": {"period": "max", "interval": "1mo"},
    }

    @classmethod
    def map_timeframe(cls, timeframe: str) -> Tuple[str, str]:
        """
        Map a timeframe string to yfinance period and interval.

        Args:
            timeframe: Timeframe string (e.g., '1m', '1h', '1d')

        Returns:
            Tuple of (period, interval)

        Raises:
            ValueError: If timeframe is not in allowed values
        """
        if not timeframe:
            raise ValueError("Timeframe cannot be empty")

        timeframe = timeframe.lower()

        if timeframe not in cls.ALLOWED_TIMEFRAMES:
            raise ValueError(
                f"Invalid timeframe: {timeframe}. "
                f"Allowed values: {', '.join(cls.ALLOWED_TIMEFRAMES)}"
            )

        mapping = cls.TIMEFRAME_MAP[timeframe]
        period = mapping["period"]
        interval = mapping["interval"]

        logger.info(
            f"Mapped timeframe {timeframe} to period={period}, interval={interval}"
        )
        return period, interval

    @classmethod
    def validate_timeframe(cls, timeframe: str) -> bool:
        """
        Validate if a timeframe value is allowed.

        Args:
            timeframe: Timeframe string to validate

        Returns:
            True if valid, False otherwise
        """
        if not timeframe:
            return False
        return timeframe.lower() in cls.ALLOWED_TIMEFRAMES


# Create a singleton instance
timeframe_mapper = TimeframeMapper()
