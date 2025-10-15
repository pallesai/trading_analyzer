"""
Unified news client that aggregates news from multiple sources (yfinance and TipRanks).
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from .tip_ranks import TipRanksNewsClient

# Import existing news clients
from .yfinance import YFNewsClient


class UnifiedNewsClient:
    """
    Unified news client that aggregates news from multiple sources.
    """

    def __init__(self, timeout: int = 30):
        """
        Initialize the unified news client.

        Args:
            timeout (int): Request timeout in seconds for API calls
        """
        self.yfinance_client = YFNewsClient()
        self.tipranks_client = TipRanksNewsClient(timeout=timeout)

    def _standardize_yfinance_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert yfinance article to standardized format.

        Args:
            article (Dict[str, Any]): Raw yfinance article

        Returns:
            Dict[str, Any]: Standardized article format
        """
        return {
            "title": article.get("title", "N/A"),
            "summary": article.get("summary", "N/A"),
            "url": article.get("link", "N/A"),
            "publisher": article.get("publisher", "N/A"),
            "published_date": article.get("published_date"),
            "sentiment": "neutral",  # yfinance doesn't provide sentiment
            "source": "yfinance",
            "ticker": None,  # Will be set by caller
            "thumbnail": article.get("thumbnail"),
            "content_type": article.get("type", "article"),
            "raw_data": article,  # Keep original data for reference
        }

    def _standardize_tipranks_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert TipRanks article to standardized format.

        Args:
            article (Dict[str, Any]): Raw TipRanks article

        Returns:
            Dict[str, Any]: Standardized article format
        """
        # Parse date from TipRanks format
        published_date = None
        if article.get("date"):
            try:
                dt = datetime.fromisoformat(article["date"].replace("Z", "+00:00"))
                published_date = dt.strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                published_date = article.get("date")

        return {
            "title": article.get("title", "N/A"),
            "summary": "N/A",  # TipRanks doesn't provide summary in this endpoint
            "url": article.get("url", article.get("urlString", "N/A")),
            "publisher": article.get("siteName", "N/A"),
            "published_date": published_date,
            "sentiment": article.get("sentiment", "neutral"),
            "source": "tipranks",
            "ticker": article.get("ticker"),
            "thumbnail": None,  # TipRanks doesn't provide thumbnails in this endpoint
            "content_type": "article",
            "company_name": article.get("companyName"),
            "raw_data": article,  # Keep original data for reference
        }

    def get_unified_news(
        self, ticker: str, limit_per_source: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get news from all sources in a unified format.

        Args:
            ticker (str): Stock ticker symbol
            limit_per_source (int): Limit articles per source (None for no limit)

        Returns:
            Dict[str, Any]: Unified response with news from all sources
        """
        unified_response = {
            "ticker": ticker.upper(),
            "sources": ["yfinance", "tipranks"],
            "total_articles": 0,
            "articles": [],
            "by_source": {
                "yfinance": {"count": 0, "articles": [], "error": None},
                "tipranks": {"count": 0, "articles": [], "error": None},
            },
            "timestamp": datetime.now().isoformat(),
        }

        # Fetch from yfinance
        try:
            yf_articles = self.yfinance_client.get_news(ticker, limit_per_source)
            standardized_yf = []
            for article in yf_articles:
                std_article = self._standardize_yfinance_article(article)
                std_article["ticker"] = ticker.upper()
                standardized_yf.append(std_article)

            unified_response["by_source"]["yfinance"]["articles"] = standardized_yf
            unified_response["by_source"]["yfinance"]["count"] = len(standardized_yf)
            unified_response["articles"].extend(standardized_yf)

        except Exception as e:
            unified_response["by_source"]["yfinance"]["error"] = str(e)

        # Fetch from TipRanks
        try:
            tr_articles = self.tipranks_client.get_news(ticker)
            if limit_per_source and len(tr_articles) > limit_per_source:
                tr_articles = tr_articles[:limit_per_source]

            standardized_tr = []
            for article in tr_articles:
                std_article = self._standardize_tipranks_article(article)
                standardized_tr.append(std_article)

            unified_response["by_source"]["tipranks"]["articles"] = standardized_tr
            unified_response["by_source"]["tipranks"]["count"] = len(standardized_tr)
            unified_response["articles"].extend(standardized_tr)

        except Exception as e:
            unified_response["by_source"]["tipranks"]["error"] = str(e)

        # Sort all articles by date (newest first)
        unified_response["articles"] = sorted(
            unified_response["articles"],
            key=lambda x: x.get("published_date", ""),
            reverse=True,
        )

        unified_response["total_articles"] = len(unified_response["articles"])

        return unified_response

    def get_news_by_source(
        self, ticker: str, source: str, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get news from a specific source only.

        Args:
            ticker (str): Stock ticker symbol
            source (str): Source name ('yfinance' or 'tipranks')
            limit (int): Limit number of articles

        Returns:
            List[Dict[str, Any]]: Standardized articles from specified source
        """
        if source.lower() == "yfinance":
            articles = self.yfinance_client.get_news(ticker, limit)
            return [self._standardize_yfinance_article(article) for article in articles]

        elif source.lower() == "tipranks":
            articles = self.tipranks_client.get_news(ticker)
            if limit and len(articles) > limit:
                articles = articles[:limit]
            return [self._standardize_tipranks_article(article) for article in articles]

        else:
            raise ValueError(
                f"Unknown source: {source}. Available sources: yfinance, tipranks"
            )

    def get_news_summary(self, ticker: str, limit_per_source: Optional[int] = 5) -> str:
        """
        Get a formatted summary of news from all sources.

        Args:
            ticker (str): Stock ticker symbol
            limit_per_source (int): Limit articles per source

        Returns:
            str: Formatted news summary
        """
        unified_news = self.get_unified_news(ticker, limit_per_source)

        summary = f"Unified News Summary for {ticker.upper()}\n"
        summary += "=" * 50 + "\n\n"

        summary += f"Total Articles: {unified_news['total_articles']}\n"
        summary += f"Sources: {', '.join(unified_news['sources'])}\n"
        summary += f"Generated: {unified_news['timestamp']}\n\n"

        # Show breakdown by source
        for source, data in unified_news["by_source"].items():
            summary += f"{source.upper()}: {data['count']} articles"
            if data["error"]:
                summary += f" (Error: {data['error']})"
            summary += "\n"

        summary += "\n" + "=" * 50 + "\n\n"

        # Show recent articles
        for i, article in enumerate(unified_news["articles"][:10], 1):  # Show top 10
            summary += f"{i}. [{article['source'].upper()}] {article['title']}\n"
            summary += f"   Publisher: {article['publisher']}\n"
            if article["published_date"]:
                summary += f"   Date: {article['published_date']}\n"
            if article["sentiment"] != "neutral":
                summary += f"   Sentiment: {article['sentiment']}\n"
            if article["summary"] and article["summary"] != "N/A":
                summary_text = article["summary"]
                if len(summary_text) > 150:
                    summary_text = summary_text[:150] + "..."
                summary += f"   Summary: {summary_text}\n"
            summary += "\n"

        return summary

    def close(self):
        """Close all client connections."""
        self.tipranks_client.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
