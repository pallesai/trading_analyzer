"""
Test script for TipRanks news client.
"""

from news.tip_ranks import TipRanksNewsClient


def test_tipranks_news():
    """Test the TipRanks news client with CCL ticker."""
    
    print("=== Testing TipRanks News Client ===\n")
    
    try:
        # Create client
        client = TipRanksNewsClient()
        
        # Test with CCL ticker
        print("Fetching news for CCL ticker...")
        news_articles = client.get_news("CCL")
        
        print(f"Found {len(news_articles)} news articles for CCL")
        
        if news_articles:
            print("\nFirst article preview:")
            first_article = news_articles[0]
            for key, value in first_article.items():
                if isinstance(value, str) and len(value) > 100:
                    print(f"{key}: {value[:100]}...")
                else:
                    print(f"{key}: {value}")
        
        # Test with details
        print("\n" + "="*50)
        print("Testing get_news_with_details...")
        details = client.get_news_with_details("CCL")
        print(f"Ticker: {details['ticker']}")
        print(f"News count: {details['news_count']}")
        
        client.close()
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"Error during test: {e}")


if __name__ == "__main__":
    test_tipranks_news()
