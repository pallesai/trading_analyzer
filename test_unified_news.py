"""
Test script for the unified news client.
"""

from news.unified_news_client import UnifiedNewsClient
import json


def test_unified_news():
    """Test the unified news client with CCL ticker."""
    
    print("=== Testing Unified News Client ===\n")
    
    try:
        # Create unified client
        client = UnifiedNewsClient()
        
        # Test unified news fetching
        print("Fetching unified news for CCL ticker...")
        unified_news = client.get_unified_news("CCL", limit_per_source=5)
        
        print(f"Total articles found: {unified_news['total_articles']}")
        print(f"Sources: {', '.join(unified_news['sources'])}")
        print(f"Timestamp: {unified_news['timestamp']}\n")
        
        # Show breakdown by source
        print("Breakdown by source:")
        for source, data in unified_news['by_source'].items():
            print(f"  {source.upper()}: {data['count']} articles")
            if data['error']:
                print(f"    Error: {data['error']}")
        print()
        
        # Show first few articles
        print("Recent articles (unified format):")
        print("-" * 50)
        for i, article in enumerate(unified_news['articles'], 1):
            print(f"{i}. [{article['source'].upper()}] {article['title']}")
            print(f"   Publisher: {article['publisher']}")
            print(f"   Date: {article['published_date']}")
            print(f"   Sentiment: {article['sentiment']}")
            print(f"   URL: {article['url'][:80]}..." if len(article['url']) > 80 else f"   URL: {article['url']}")
            print()
        
        # Test source-specific fetching
        print("=" * 60)
        print("Testing source-specific fetching...")
        
        yf_articles = client.get_news_by_source("CCL", "yfinance", limit=2)
        print(f"YFinance articles: {len(yf_articles)}")
        
        tr_articles = client.get_news_by_source("CCL", "tipranks", limit=2)
        print(f"TipRanks articles: {len(tr_articles)}")
        
        # Test summary
        print("\n" + "=" * 60)
        print("Testing news summary...")
        summary = client.get_news_summary("CCL", limit_per_source=3)
        print(summary[:500] + "..." if len(summary) > 500 else summary)
        
        client.close()
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"Error during test: {e}")


if __name__ == "__main__":
    test_unified_news()
