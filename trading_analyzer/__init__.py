"""
Trading Analyzer - A comprehensive trading analysis toolkit.

This package provides tools for:
- Multi-source news aggregation (YFinance, TipRanks)
- Market data analysis
- HTTP client utilities
- Trading API integrations
"""

__version__ = "0.1.0"
__author__ = "Trading Analyzer Team"
__email__ = "contact@trading-analyzer.com"

# Import main classes for easy access
from http_client.client import HTTPClient
from news.unified_news_client import UnifiedNewsClient

__all__ = [
    "UnifiedNewsClient",
    "HTTPClient",
    "__version__",
]
