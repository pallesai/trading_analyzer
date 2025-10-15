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
```

## IntelliJ IDEA Setup (macOS)
1. Open IntelliJ IDEA
2. File → Open → Select this project folder
3. Configure Python interpreter:
   - IntelliJ IDEA → Preferences → Project → Python Interpreter
   - Click gear icon → Add → Virtualenv Environment → Existing environment
   - Point to `venv/bin/python` in your project folder
4. Run files:
   - Right-click `test_news_simple.py` → Run 'test_news_simple'
   - Or use green play button in toolbar
   - Or press Ctrl+Shift+R

## Terminal Commands (macOS)
```bash
# Navigate to project folder
cd /path/to/trading_analyzer

# Activate virtual environment
source venv/bin/activate

# Run test
python test_news_simple.py
```
