"""Simple test for news API functionality."""

from news import NewsClient

def test_news_api():
    """Test basic news API functionality."""
    print("Testing News API...\n")
    
    client = NewsClient()
    
    # Test 1: Get news headlines
    print("1. Testing news headlines for TSLA:")
    try:
        headlines = client.get_news_headlines("TSLA", limit=3)
        if headlines:
            for i, headline in enumerate(headlines, 1):
                print(f"   {i}. {headline}")
        else:
            print("   No headlines found")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "-"*50 + "\n")
    
    # Test 2: Get detailed news
    print("2. Testing detailed news for NVDA:")
    try:
        news = client.get_news("NVDA", limit=2)
        if news:
            for i, article in enumerate(news, 1):
                print(f"   {i}. {article['title']}")
                print(f"      Publisher: {article['publisher']}")
                print(f"      Date: {article['published_date']}")
                print()
        else:
            print("   No news found")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("-"*50)
    print("News API test completed!")

if __name__ == "__main__":
    test_news_api()
