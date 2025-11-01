#!/usr/bin/env python
"""
CLI script to refresh NIFTY 500 universe from NSE

Usage:
    python -m scripts.refresh_nifty500 [--save-to-config] [--timeout SECONDS]
"""

import argparse
import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.indian_stock_service import IndianStockService


def main():
    parser = argparse.ArgumentParser(
        description='Refresh NIFTY 500 universe from NSE',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m scripts.refresh_nifty500
  python -m scripts.refresh_nifty500 --save-to-config
  python -m scripts.refresh_nifty500 --save-to-config --timeout 60
        """
    )
    
    parser.add_argument(
        '--save-to-config',
        action='store_true',
        help='Save to tracked config file (config/nse_nifty500.json) in addition to cache'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=30,
        help='Timeout in seconds for HTTP requests (default: 30)'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("NIFTY 500 Universe Refresh")
    print("=" * 60)
    print()
    
    # Create service instance
    print("Initializing Indian Stock Service...")
    service = IndianStockService()
    print(f"Current universe size: {len(service.indian_stocks)} stocks")
    print()
    
    # Refresh universe
    print("Fetching latest NIFTY 500 data from NSE...")
    result = service.refresh_universe(save_to_config=args.save_to_config, timeout=args.timeout)
    
    # Print human-readable summary
    print()
    print("=" * 60)
    print("REFRESH SUMMARY")
    print("=" * 60)
    
    if result["updated"]:
        print(f"✓ Successfully updated universe")
        print(f"  Total stocks: {result['total']}")
        print(f"  Source: {result['source']}")
        print(f"  Cache saved: {'Yes' if result['saved_cache'] else 'No'}")
        print(f"  Config saved: {'Yes' if result['saved_config'] else 'No'}")
        print(f"  Timestamp: {result['timestamp']}")
        
        if result.get("errors"):
            print(f"\n⚠ Warnings:")
            for error in result["errors"]:
                print(f"  - {error}")
    else:
        print(f"✗ Failed to update universe")
        print(f"  Current stocks: {result['total']}")
        
        if result.get("errors"):
            print(f"\n✗ Errors:")
            for error in result["errors"]:
                print(f"  - {error}")
    
    print()
    print("=" * 60)
    
    # Echo JSON summary
    print("\nJSON Summary:")
    print(json.dumps(result, indent=2))
    
    # Exit with appropriate code
    sys.exit(0 if result["updated"] else 1)


if __name__ == "__main__":
    main()
