"""Simple test for news API functionality."""

from trading_analyzer.news.news_client import NewsClient


def test_news_api():
    """Test basic news API functionality."""
    print("Testing News API...\n")

    client = NewsClient()

    # Test 2: Get detailed news
    print("2. Testing detailed news for NVDA:")
    try:
        news = client.get_news("NVDA", limit=10)

        for i in news:
            print(f" Article --> {i}")
            print()

    except Exception as e:
        print(f"   Error: {e}")

    print("-" * 50)
    print("News API test completed!")


if __name__ == "__main__":
    test_news_api()
