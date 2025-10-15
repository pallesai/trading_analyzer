# Trading Analyzer

Yahoo Finance data access with Python.

## Install
```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
# OR manually:
pip install yfinance pandas
```

## Troubleshooting
If you get `ModuleNotFoundError: No module named 'yfinance'`:
1. Make sure virtual environment is activated: `source venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. In IntelliJ IDEA, verify Python interpreter points to `venv/bin/python`

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

## Verify Installation
```bash
# Check if dependencies are installed
python -c "import yfinance, pandas; print('✓ All dependencies installed')"
```

## Test
```bash
python test_news_simple.py
