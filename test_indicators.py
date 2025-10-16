#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

print("Testing indicator services...")

try:
    from services.volatility_indicators_service import volatility_indicators_service
    
    # Test with sample data
    highs = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115]
    lows = [99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114]
    closes = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115]
    
    result = volatility_indicators_service.calculate_atr(highs, lows, closes, 14)
    print(f"✓ ATR calculated successfully: {result}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
