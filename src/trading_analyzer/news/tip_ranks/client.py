"""
TipRanks news client for fetching stock news by ticker.
"""

import os
import sys
from typing import Any, Dict, List, Optional

# Add the parent directory to the path to import http_client
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from http_client import HTTPClient

# API Constants
API_ENDPOINTS = {
    'GET_NEWS': 'api/stocks/getNews'
}


class TipRanksNewsClient:
    """
    Client for fetching news from TipRanks API.
    """
    
    def __init__(self, timeout: int = 30):
        """
        Initialize the TipRanks news client.
        
        Args:
            timeout (int): Request timeout in seconds
        """
        self.base_url = "https://www.tipranks.com"
        self.http_client = HTTPClient(base_url=self.base_url, timeout=timeout)
    
    def get_news(self, ticker: str) -> List[Dict[str, Any]]:
        """
        Fetch news for a specific stock ticker from TipRanks.
        
        Args:
            ticker (str): Stock ticker symbol (e.g., 'CCL', 'AAPL', 'TSLA')
            
        Returns:
            List[Dict[str, Any]]: List of news articles
            
        Raises:
            requests.RequestException: If the API request fails
            ValueError: If ticker is empty or invalid
        """
        if not ticker or not isinstance(ticker, str):
            raise ValueError("Ticker must be a non-empty string")
        
        ticker = ticker.upper().strip()
        
        try:
            endpoint = API_ENDPOINTS['GET_NEWS']
            params = {'ticker': ticker}
            response_data = self.http_client.get_json(endpoint, params=params)
            
            # TipRanks API typically returns news in a specific format
            # Extract the news articles from the response
            if isinstance(response_data, dict):
                # Check if response has news data
                news_articles = response_data.get('news', [])
                if not news_articles and 'data' in response_data:
                    news_articles = response_data.get('data', [])
                
                return news_articles if isinstance(news_articles, list) else []
            elif isinstance(response_data, list):
                # If response is directly a list of articles
                return response_data
            else:
                return []
                
        except Exception as e:
            raise Exception(f"Failed to fetch news for ticker {ticker}: {str(e)}")
    
    def close(self):
        """Close the HTTP client session."""
        self.http_client.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
