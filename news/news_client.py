"""News client for stock news retrieval using Yahoo Finance API."""

import yfinance as yf
from typing import Optional, List, Dict, Any
from datetime import datetime


class NewsClient:
    """
    A client for retrieving stock news from Yahoo Finance API.
    
    This class provides access to recent news articles related to specific stock symbols.
    News data includes headlines, summaries, publication dates, and source links.
    
    The client uses the yfinance library which accesses Yahoo Finance's public news API.
    All methods include proper error handling and return structured data.
    
    Example:
        >>> from news import NewsClient
        >>> client = NewsClient()
        >>> news = client.get_news("AAPL", limit=5)
        >>> summary = client.get_news_summary("AAPL", limit=3)
    
    Note:
        - News data availability varies significantly by symbol
        - Major stocks typically have more comprehensive news coverage
        - Articles are typically from the last few days to weeks
        - Some symbols may have no recent news available
    """
    
    def __init__(self):
        """
        Initialize the News client.
        
        No authentication is required as this uses Yahoo Finance's public API.
        The client is stateless and can be reused for multiple requests.
        """
        pass
    
    def get_news(self, symbol: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get recent news articles for a stock from Yahoo Finance API.
        
        Retrieves the latest news articles related to a specific stock symbol.
        News data includes headlines, summaries, publication dates, and source links.
        
        API Endpoint: Uses yfinance ticker.news property
        Rate Limit: No explicit limit, but excessive requests may be throttled
        Data Freshness: Updated in real-time as news is published
        Coverage: Varies by symbol; major stocks have more comprehensive coverage
        
        Args:
            symbol (str): Stock ticker symbol (e.g., 'AAPL', 'TSLA', 'GOOGL')
            limit (Optional[int]): Maximum number of articles to return.
                                 If None, returns all available articles (typically 10-20)
            
        Returns:
            List[Dict[str, Any]]: List of news article dictionaries with keys:
                - title (str): Article headline
                - summary (str): Article summary/description
                - link (str): URL to full article
                - publisher (str): News source/publisher name
                - published_date (str): Publication date in 'YYYY-MM-DD HH:MM:SS' format
                - type (str): Article type/category
                - thumbnail (Optional[str]): URL to article thumbnail image
                
        Raises:
            Exception: If symbol is invalid or API request fails
            
        Example:
            >>> client = NewsClient()
            >>> news = client.get_news("AAPL", limit=5)
            >>> for article in news:
            ...     print(f"Title: {article['title']}")
            ...     print(f"Publisher: {article['publisher']}")
            ...     print(f"Date: {article['published_date']}")
            
        Note:
            - News availability varies significantly by symbol
            - Some symbols may have no recent news
            - Articles are typically from the last few days to weeks
        """
        try:
            ticker = yf.Ticker(symbol)
            news = ticker.news
            
            if not news:
                return []
            
            # Apply limit if specified
            if limit and len(news) > limit:
                news = news[:limit]
            
            # Clean up and format news data - Updated for new yfinance structure
            formatted_news = []
            for article in news:
                # Handle the new nested structure where data is under 'content'
                if article is None:
                    continue
                content = article.get('content', article)  # Fallback to article if no content key
                if content is None:
                    continue
                
                formatted_article = {
                    'title': content.get('title', 'N/A'),
                    'summary': content.get('summary', content.get('description', 'N/A')),
                    'link': content.get('clickThroughUrl', {}).get('url', content.get('canonicalUrl', {}).get('url', 'N/A')),
                    'publisher': content.get('provider', {}).get('displayName', 'N/A'),
                    'published_date': content.get('pubDate', content.get('displayTime', None)),
                    'type': content.get('contentType', 'N/A'),
                    'thumbnail': None
                }
                
                # Handle thumbnail URL
                thumbnail_data = content.get('thumbnail', {})
                if thumbnail_data and 'resolutions' in thumbnail_data:
                    resolutions = thumbnail_data['resolutions']
                    if resolutions and len(resolutions) > 0:
                        formatted_article['thumbnail'] = resolutions[0].get('url', None)
                
                # Convert ISO date string to readable format if available
                if formatted_article['published_date']:
                    try:
                        # Handle ISO format dates (e.g., "2025-10-15T05:00:35Z")
                        if isinstance(formatted_article['published_date'], str):
                            # Parse ISO format
                            dt = datetime.fromisoformat(formatted_article['published_date'].replace('Z', '+00:00'))
                            formatted_article['published_date'] = dt.strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        # If parsing fails, keep original value
                        pass
                
                formatted_news.append(formatted_article)
            
            return formatted_news
            
        except Exception as e:
            raise Exception(f"Error fetching news for {symbol}: {str(e)}")
    
    def get_news_summary(self, symbol: str, limit: int = 5) -> str:
        """
        Get a formatted summary of recent news for a stock.
        
        Provides a human-readable summary of recent news articles with titles,
        publishers, dates, summaries, and links formatted for easy reading.
        
        Args:
            symbol (str): Stock ticker symbol (e.g., 'AAPL', 'TSLA', 'GOOGL')
            limit (int): Maximum number of news articles to include (default: 5)
            
        Returns:
            str: Formatted string with news summary including:
                - Article titles and numbering
                - Publisher information
                - Publication dates
                - Article summaries (truncated if long)
                - Direct links to full articles
                
        Raises:
            Exception: If symbol is invalid or API request fails
            
        Example:
            >>> client = NewsClient()
            >>> summary = client.get_news_summary("AAPL", limit=3)
            >>> print(summary)
            
        Note:
            - Returns a user-friendly message if no news is found
            - Long summaries are automatically truncated to 200 characters
            - All errors are handled gracefully with descriptive messages
        """
        try:
            news = self.get_news(symbol, limit)
            
            if not news:
                return f"No recent news found for {symbol}"
            
            summary = f"Recent News for {symbol}:\n"
            summary += "=" * 50 + "\n\n"
            
            for i, article in enumerate(news, 1):
                summary += f"{i}. {article['title']}\n"
                summary += f"   Publisher: {article['publisher']}\n"
                if article['published_date']:
                    summary += f"   Date: {article['published_date']}\n"
                if article['summary'] and article['summary'] != 'N/A':
                    # Truncate long summaries
                    summary_text = article['summary']
                    if len(summary_text) > 200:
                        summary_text = summary_text[:200] + "..."
                    summary += f"   Summary: {summary_text}\n"
                if article['link'] and article['link'] != 'N/A':
                    summary += f"   Link: {article['link']}\n"
                summary += "\n"
            
            return summary
            
        except Exception as e:
            return f"Error fetching news summary for {symbol}: {str(e)}"
    
    def get_news_headlines(self, symbol: str, limit: int = 10) -> List[str]:
        """
        Get just the headlines from recent news articles.
        
        A convenience method that returns only the article titles,
        useful for quick news scanning or when you only need headlines.
        
        Args:
            symbol (str): Stock ticker symbol (e.g., 'AAPL', 'TSLA', 'GOOGL')
            limit (int): Maximum number of headlines to return (default: 10)
            
        Returns:
            List[str]: List of article headlines/titles
            
        Raises:
            Exception: If symbol is invalid or API request fails
            
        Example:
            >>> client = NewsClient()
            >>> headlines = client.get_news_headlines("AAPL", limit=5)
            >>> for headline in headlines:
            ...     print(f"• {headline}")
        """
        try:
            news = self.get_news(symbol, limit)
            return [article['title'] for article in news if article['title'] != 'N/A']
        except Exception as e:
            raise Exception(f"Error fetching news headlines for {symbol}: {str(e)}")
    
    def search_news_by_keyword(self, symbol: str, keyword: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for news articles containing a specific keyword.
        
        Filters news articles to only include those that contain the specified
        keyword in either the title or summary.
        
        Args:
            symbol (str): Stock ticker symbol (e.g., 'AAPL', 'TSLA', 'GOOGL')
            keyword (str): Keyword to search for (case-insensitive)
            limit (int): Maximum number of articles to search through (default: 10)
            
        Returns:
            List[Dict[str, Any]]: List of matching news articles with same structure as get_news()
            
        Raises:
            Exception: If symbol is invalid or API request fails
            
        Example:
            >>> client = NewsClient()
            >>> earnings_news = client.search_news_by_keyword("AAPL", "earnings", limit=20)
            >>> for article in earnings_news:
            ...     print(f"Found: {article['title']}")
        """
        try:
            news = self.get_news(symbol, limit)
            keyword_lower = keyword.lower()
            
            matching_articles = []
            for article in news:
                title = article.get('title', '').lower()
                summary = article.get('summary', '').lower()
                
                if keyword_lower in title or keyword_lower in summary:
                    matching_articles.append(article)
            
            return matching_articles
            
        except Exception as e:
            raise Exception(f"Error searching news for {symbol} with keyword '{keyword}': {str(e)}")
