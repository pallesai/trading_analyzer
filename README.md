# Trading Analyzer

Yahoo Finance data access with Python.

## Install
```bash
pip install yfinance pandas
```

## Usage
```python
from trading_api import YFinanceClient
from news import NewsClient

# Stock data
client = YFinanceClient()
price = client.get_current_price("AAPL")
data = client.get_historical_data("AAPL", period="1y")

# News
news_client = NewsClient()
headlines = news_client.get_news_headlines("AAPL", limit=5)
```

## Test
```bash
python test_news_simple.py
