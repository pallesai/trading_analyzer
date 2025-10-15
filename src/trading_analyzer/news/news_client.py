"""News client for stock news retrieval using Yahoo Finance API."""

from datetime import datetime
from typing import Any, Dict, List, Optional

import yfinance as yf


class NewsClient:
    """Yahoo Finance news client."""
    
    def __init__(self):
        """Initialize the News client."""
        pass
    
    def get_news(self, symbol: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get recent news articles."""
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
                
                # Handle clickThroughUrl which can be None or a dict
                click_through = content.get('clickThroughUrl')
                if click_through and isinstance(click_through, dict):
                    link = click_through.get('url', 'N/A')
                else:
                    canonical = content.get('canonicalUrl', {})
                    link = canonical.get('url', 'N/A') if canonical else 'N/A'
                
                formatted_article = {
                    'title': content.get('title', 'N/A'),
                    'summary': content.get('summary', content.get('description', 'N/A')),
                    'link': link,
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
        """Get formatted news summary."""
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
        """Get news headlines only."""
        try:
            news = self.get_news(symbol, limit)
            return [article['title'] for article in news if article['title'] != 'N/A']
        except Exception as e:
            raise Exception(f"Error fetching news headlines for {symbol}: {str(e)}")
    
    def search_news_by_keyword(self, symbol: str, keyword: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search news by keyword."""
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
