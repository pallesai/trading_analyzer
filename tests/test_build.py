"""
Build verification script to test all components of the trading analyzer.
"""

import sys
import traceback


def test_imports():
    """Test that all modules can be imported correctly."""
    print("Testing imports...")

    try:
        # Test HTTP client
        from trading_analyzer.http_client.client import HTTPClient  # noqa: F401

        print("✓ HTTP client import successful")

        # Test news clients
        from trading_analyzer.news.yfinance import YFNewsClient  # noqa: F401

        print("✓ YFinance news client import successful")

        from trading_analyzer.news.tip_ranks import TipRanksNewsClient  # noqa: F401

        print("✓ TipRanks news client import successful")

        from trading_analyzer.news.unified_news_client import (  # noqa: F401
            UnifiedNewsClient,
        )

        print("✓ Unified news client import successful")

        # Test trading API
        from trading_analyzer.trading_api.yfinance_client import (  # noqa: F401
            YFinanceClient,
        )

        print("✓ YFinance trading client import successful")

        return True

    except Exception as e:
        print(f"✗ Import failed: {e}")
        traceback.print_exc()
        return False


def test_basic_functionality():
    """Test basic functionality of key components."""
    print("\nTesting basic functionality...")

    try:
        # Test HTTP client
        from trading_analyzer.http_client.client import HTTPClient

        client = HTTPClient()
        print("✓ HTTP client instantiation successful")
        client.close()

        # Test news clients
        from trading_analyzer.news.yfinance import YFNewsClient

        news_client = YFNewsClient()  # noqa: F841
        print("✓ YFinance news client instantiation successful")

        from trading_analyzer.news.tip_ranks import TipRanksNewsClient

        tr_client = TipRanksNewsClient()
        print("✓ TipRanks news client instantiation successful")
        tr_client.close()

        from trading_analyzer.news.unified_news_client import UnifiedNewsClient

        unified_client = UnifiedNewsClient()
        print("✓ Unified news client instantiation successful")
        unified_client.close()

        return True

    except Exception as e:
        print(f"✗ Functionality test failed: {e}")
        traceback.print_exc()
        return False


def test_dependencies():
    """Test that all required dependencies are available."""
    print("Testing dependencies...")

    required_packages = ["yfinance", "pandas", "requests"]

    all_available = True

    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is available")
        except ImportError:
            print(f"✗ {package} is missing")
            all_available = False

    return all_available


def main():
    """Run all build verification tests."""
    print("=" * 60)
    print("TRADING ANALYZER BUILD VERIFICATION")
    print("=" * 60)

    tests = [
        ("Dependencies", test_dependencies),
        ("Imports", test_imports),
        ("Basic Functionality", test_basic_functionality),
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n{test_name.upper()} TEST:")
        print("-" * 40)
        result = test_func()
        results.append((test_name, result))

    print("\n" + "=" * 60)
    print("BUILD VERIFICATION SUMMARY")
    print("=" * 60)

    all_passed = True
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED - BUILD IS SUCCESSFUL!")
        print("The trading analyzer is ready to use.")
    else:
        print("❌ SOME TESTS FAILED - BUILD NEEDS ATTENTION")
        print("Please check the errors above and fix them.")
    print("=" * 60)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
