"""
Modern build verification script for pyproject.toml-based trading analyzer.
"""

import subprocess
import sys
import traceback
from pathlib import Path


def run_command(command: str, description: str) -> bool:
    """Run a command and return success status."""
    print(f"Running: {description}")
    try:
        result = subprocess.run(
            command.split(), capture_output=True, text=True, check=True
        )
        print(f"✓ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} - FAILED")
        print(f"Error: {e.stderr}")
        return False
    except Exception as e:
        print(f"✗ {description} - ERROR: {e}")
        return False


def test_imports():
    """Test that all modules can be imported correctly."""
    print("\nTesting imports...")

    try:
        # Test HTTP client
        from trading_analyzer.http_client.client import HTTPClient

        print("✓ HTTP client import successful")

        # Test news clients
        from trading_analyzer.news.news_client import NewsClient

        print("✓ YFinance news client import successful")

        from trading_analyzer.news.tip_ranks import TipRanksNewsClient

        print("✓ TipRanks news client import successful")

        from trading_analyzer.news.unified_news_client import UnifiedNewsClient

        print("✓ Unified news client import successful")

        # Test trading API
        from trading_analyzer.trading_api.yfinance_client import YFinanceClient

        print("✓ YFinance trading client import successful")

        # Test main package
        import trading_analyzer

        print(f"✓ Main package import successful (v{trading_analyzer.__version__})")

        return True

    except Exception as e:
        print(f"✗ Import failed: {e}")
        traceback.print_exc()
        return False


def test_build_system():
    """Test the modern build system."""
    print("\nTesting build system...")

    # Check if pyproject.toml exists
    if not Path("pyproject.toml").exists():
        print("✗ pyproject.toml not found")
        return False
    print("✓ pyproject.toml found")

    # Test package installation in development mode
    success = run_command("pip install -e .", "Development installation")
    if not success:
        return False

    return True


def test_code_quality():
    """Test code quality tools."""
    print("\nTesting code quality tools...")

    results = []

    # Test black (code formatting)
    results.append(
        run_command("black --check --diff .", "Code formatting check (black)")
    )

    # Test isort (import sorting)
    results.append(
        run_command("isort --check-only --diff .", "Import sorting check (isort)")
    )

    # Test flake8 (linting)
    results.append(
        run_command("flake8 . --count --statistics", "Code linting (flake8)")
    )

    return all(results)


def test_pytest():
    """Test pytest execution."""
    print("\nTesting pytest...")

    return run_command("pytest tests/ -v --tb=short", "Running pytest tests")


def test_package_build():
    """Test package building."""
    print("\nTesting package building...")

    # Install build tool if not present
    run_command("pip install build", "Installing build tool")

    # Build the package
    return run_command("python -m build", "Building package")


def main():
    """Run all build verification tests."""
    print("=" * 70)
    print("MODERN TRADING ANALYZER BUILD VERIFICATION")
    print("=" * 70)

    tests = [
        ("Build System", test_build_system),
        ("Imports", test_imports),
        ("Code Quality", test_code_quality),
        ("Pytest Tests", test_pytest),
        ("Package Build", test_package_build),
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n{test_name.upper()} TEST:")
        print("-" * 50)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} test failed with exception: {e}")
            results.append((test_name, False))

    print("\n" + "=" * 70)
    print("BUILD VERIFICATION SUMMARY")
    print("=" * 70)

    all_passed = True
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name:20}: {status}")
        if not result:
            all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 ALL TESTS PASSED - MODERN BUILD IS SUCCESSFUL!")
        print("Your trading analyzer is now using modern Python best practices:")
        print("  • pyproject.toml configuration")
        print("  • pytest testing framework")
        print("  • Code quality tools (black, flake8, isort)")
        print("  • Professional package structure")
        print("  • CI/CD ready with GitHub Actions")
    else:
        print("❌ SOME TESTS FAILED - BUILD NEEDS ATTENTION")
        print("Please check the errors above and fix them.")
    print("=" * 70)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
