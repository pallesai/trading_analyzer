# Trading Analyzer with YFinance Integration

A comprehensive Python toolkit that provides easy access to Yahoo Finance data through the yfinance library. The project is organized into two main modules: **trading_api** for stock data and analysis, and **news** for stock news retrieval.

## Features

### Trading API Module
- **Stock Information**: Get basic company information, market cap, P/E ratios, etc.
- **Historical Data**: Fetch historical price data with customizable periods and intervals
- **Current Prices**: Get real-time stock prices
- **Multiple Stocks**: Fetch data for multiple stocks at once
- **Technical Analysis**: Calculate returns, moving averages, and volatility
- **Dividend & Split Data**: Access dividend and stock split history

### News API Module
- **Recent News**: Get latest news articles for any stock symbol
- **News Headlines**: Quick access to just the headlines
- **News Summaries**: Formatted, readable news summaries
- **Keyword Search**: Search news articles by specific keywords
- **Publisher Information**: Access to news sources and publication dates

## Installation

1. Make sure you have Python 3.8+ installed
2. Install the required dependencies:
```bash
pip install yfinance pandas
```

## Usage

### Basic Import
```python
from trading_api import YFinanceClient
from news import NewsClient

# Initialize the clients
trading_client = YFinanceClient()
news_client = NewsClient()
```

### Get Stock Information
```python
# Get basic company information
info = client.get_stock_info("AAPL")
print(f"Company: {info['longName']}")
print(f"Sector: {info['sector']}")
print(f"Market Cap: ${info['marketCap']:,}")
```

### Get Current Price
```python
# Get current stock price
price = client.get_current_price("AAPL")
print(f"AAPL current price: ${price:.2f}")
```

### Get Historical Data
```python
# Get historical data for different periods
data = client.get_historical_data("AAPL", period="1y")  # 1 year
data = client.get_historical_data("AAPL", start="2023-01-01", end="2023-12-31")  # Custom dates
data = client.get_historical_data("AAPL", period="1mo", interval="1h")  # Hourly data
```

### Calculate Returns
```python
# Get historical data
data = client.get_historical_data("AAPL", period="3mo")

# Calculate different types of returns
daily_returns = client.calculate_returns(data, "daily")
weekly_returns = client.calculate_returns(data, "weekly")
monthly_returns = client.calculate_returns(data, "monthly")
```

### Moving Averages
```python
# Calculate moving averages
data = client.get_historical_data("AAPL", period="6mo")
ma_data = client.get_moving_averages(data, [20, 50, 200])

# Access the moving averages
print(f"20-day MA: ${ma_data['MA_20'].iloc[-1]:.2f}")
print(f"50-day MA: ${ma_data['MA_50'].iloc[-1]:.2f}")
print(f"200-day MA: ${ma_data['MA_200'].iloc[-1]:.2f}")
```

### Volatility Analysis
```python
# Calculate rolling volatility
data = client.get_historical_data("AAPL", period="1y")
volatility = client.get_volatility(data, window=30)
print(f"Current 30-day volatility: {volatility.iloc[-1]:.2f}")
```

### Multiple Stocks
```python
# Get data for multiple stocks
symbols = ["AAPL", "GOOGL", "MSFT", "TSLA"]
stock_data = client.get_multiple_stocks(symbols, period="3mo")

# Compare performance
for symbol, data in stock_data.items():
    if not data.empty:
        start_price = data['Close'].iloc[0]
        end_price = data['Close'].iloc[-1]
        performance = ((end_price - start_price) / start_price) * 100
        print(f"{symbol}: {performance:+.2f}%")
```

### Dividends and Splits
```python
# Get dividend history
dividends = client.get_dividends("AAPL")
print(dividends.tail())

# Get stock split history
splits = client.get_splits("AAPL")
print(splits.tail())
```

### News API
```python
# Get recent news articles (formatted summary)
news_summary = client.get_news_summary("AAPL", limit=5)
print(news_summary)

# Get raw news data
news_data = client.get_news("AAPL", limit=3)
for article in news_data:
    print(f"Title: {article['title']}")
    print(f"Publisher: {article['publisher']}")
    print(f"Date: {article['published_date']}")
    print(f"Link: {article['link']}")
    print("---")
```

## Available Methods

### YFinanceClient Methods

- `get_stock_info(symbol)` - Get basic stock information
- `get_historical_data(symbol, period, start, end, interval)` - Get historical price data
- `get_multiple_stocks(symbols, period, start, end)` - Get data for multiple stocks
- `get_current_price(symbol)` - Get current stock price
- `get_dividends(symbol)` - Get dividend history
- `get_splits(symbol)` - Get stock split history
- `calculate_returns(data, period)` - Calculate returns (daily, weekly, monthly)
- `get_moving_averages(data, windows)` - Calculate moving averages
- `get_volatility(data, window)` - Calculate rolling volatility
- `get_news(symbol, limit)` - Get recent news articles for a stock
- `get_news_summary(symbol, limit)` - Get formatted news summary

### Parameters

**Periods**: `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`

**Intervals**: `1m`, `2m`, `5m`, `15m`, `30m`, `60m`, `90m`, `1h`, `1d`, `5d`, `1wk`, `1mo`, `3mo`

## Example Script

Run the included example script to see all features in action:

```bash
python example_usage.py
```

This will demonstrate:
- Fetching stock information
- Getting current prices
- Historical data analysis
- Return calculations
- Moving averages
- Volatility analysis
- Multi-stock comparisons

## Error Handling

All methods include proper error handling and will raise exceptions with descriptive messages if something goes wrong. Always wrap your calls in try-except blocks for production use:

```python
try:
    data = client.get_historical_data("INVALID_SYMBOL")
except Exception as e:
    print(f"Error: {e}")
```

## Requirements

- Python 3.8+
- yfinance
- pandas
- numpy (installed automatically with pandas)

## License

This project is open source and available under the MIT License.
