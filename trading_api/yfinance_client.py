"""YFinance client for stock data retrieval and analysis."""

import yfinance as yf
import pandas as pd
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta


class YFinanceClient:
    """
    A client for interacting with Yahoo Finance API through yfinance.
    
    This class provides a comprehensive interface to Yahoo Finance data including:
    - Stock information and current prices
    - Historical price data with flexible periods and intervals
    - Technical analysis tools (returns, moving averages, volatility)
    - Corporate actions (dividends, stock splits)
    - Multi-stock data retrieval and comparison
    
    Note: News functionality has been moved to a separate news module.
    Use the NewsClient from the news module for news-related features.
    
    The client uses the yfinance library which accesses Yahoo Finance's public API.
    All methods include proper error handling and return structured data.
    
    Example:
        >>> from trading_api import YFinanceClient
        >>> from news import NewsClient
        >>> 
        >>> client = YFinanceClient()
        >>> news_client = NewsClient()
        >>> 
        >>> price = client.get_current_price("AAPL")
        >>> data = client.get_historical_data("AAPL", period="1y")
        >>> news = news_client.get_news_summary("AAPL", limit=5)
    
    Available Data Periods:
        - 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    
    Available Data Intervals:
        - 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
    
    Note:
        - Intraday data (< 1d intervals) is limited to last 60 days
        - Some data may be delayed by 15-20 minutes
        - Rate limiting may apply for excessive requests
    """
    
    def __init__(self):
        """
        Initialize the YFinance client.
        
        No authentication is required as this uses Yahoo Finance's public API.
        The client is stateless and can be reused for multiple requests.
        """
        pass
    
    def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        """
        Get basic information about a stock from Yahoo Finance API.
        
        Retrieves comprehensive company information including market cap, P/E ratio,
        sector, industry, business summary, and other fundamental data.
        
        API Endpoint: Uses yfinance ticker.info property
        Rate Limit: No explicit limit, but excessive requests may be throttled
        Data Freshness: Updated during market hours, may be delayed 15-20 minutes
        
        Args:
            symbol (str): Stock ticker symbol (e.g., 'AAPL', 'GOOGL', 'MSFT')
                         Case insensitive, but uppercase recommended
            
        Returns:
            Dict[str, Any]: Dictionary containing stock information with keys like:
                - longName: Company full name
                - sector: Business sector
                - industry: Specific industry
                - marketCap: Market capitalization
                - trailingPE: Price-to-earnings ratio
                - dividendYield: Dividend yield percentage
                - beta: Stock beta (volatility vs market)
                - And many more financial metrics
                
        Raises:
            Exception: If symbol is invalid or API request fails
            
        Example:
            >>> client = YFinanceClient()
            >>> info = client.get_stock_info("AAPL")
            >>> print(f"Company: {info['longName']}")
            >>> print(f"Market Cap: ${info['marketCap']:,}")
        """
        try:
            ticker = yf.Ticker(symbol)
            return ticker.info
        except Exception as e:
            raise Exception(f"Error fetching info for {symbol}: {str(e)}")
    
    def get_historical_data(
        self, 
        symbol: str, 
        period: str = "1y",
        start: Optional[str] = None,
        end: Optional[str] = None,
        interval: str = "1d"
    ) -> pd.DataFrame:
        """
        Get historical stock data.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'GOOGL')
            period: Period to download (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            start: Start date string (YYYY-MM-DD) - optional
            end: End date string (YYYY-MM-DD) - optional
            interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
            
        Returns:
            DataFrame with historical data (Open, High, Low, Close, Volume, etc.)
        """
        try:
            ticker = yf.Ticker(symbol)
            if start and end:
                data = ticker.history(start=start, end=end, interval=interval)
            else:
                data = ticker.history(period=period, interval=interval)
            
            if data.empty:
                raise Exception(f"No data found for symbol {symbol}")
                
            return data
        except Exception as e:
            raise Exception(f"Error fetching historical data for {symbol}: {str(e)}")
    
    def get_multiple_stocks(
        self, 
        symbols: List[str], 
        period: str = "1y",
        start: Optional[str] = None,
        end: Optional[str] = None
    ) -> Dict[str, pd.DataFrame]:
        """
        Get historical data for multiple stocks.
        
        Args:
            symbols: List of stock symbols
            period: Period to download
            start: Start date string (YYYY-MM-DD) - optional
            end: End date string (YYYY-MM-DD) - optional
            
        Returns:
            Dictionary with symbol as key and DataFrame as value
        """
        results = {}
        for symbol in symbols:
            try:
                results[symbol] = self.get_historical_data(symbol, period, start, end)
            except Exception as e:
                print(f"Warning: Could not fetch data for {symbol}: {str(e)}")
                results[symbol] = pd.DataFrame()
        
        return results
    
    def get_current_price(self, symbol: str) -> float:
        """
        Get current stock price.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Current stock price
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d", interval="1m")
            if data.empty:
                # Fallback to daily data
                data = ticker.history(period="1d")
            
            if data.empty:
                raise Exception(f"No current price data available for {symbol}")
                
            return float(data['Close'].iloc[-1])
        except Exception as e:
            raise Exception(f"Error fetching current price for {symbol}: {str(e)}")
    
    def get_dividends(self, symbol: str) -> pd.DataFrame:
        """
        Get dividend history for a stock.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            DataFrame with dividend history
        """
        try:
            ticker = yf.Ticker(symbol)
            dividends = ticker.dividends
            return dividends.to_frame('Dividend') if not dividends.empty else pd.DataFrame()
        except Exception as e:
            raise Exception(f"Error fetching dividends for {symbol}: {str(e)}")
    
    def get_splits(self, symbol: str) -> pd.DataFrame:
        """
        Get stock split history.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            DataFrame with split history
        """
        try:
            ticker = yf.Ticker(symbol)
            splits = ticker.splits
            return splits.to_frame('Split') if not splits.empty else pd.DataFrame()
        except Exception as e:
            raise Exception(f"Error fetching splits for {symbol}: {str(e)}")
    
    def calculate_returns(self, data: pd.DataFrame, period: str = "daily") -> pd.Series:
        """
        Calculate returns from price data.
        
        Args:
            data: DataFrame with price data (must have 'Close' column)
            period: Type of returns ('daily', 'weekly', 'monthly')
            
        Returns:
            Series with calculated returns
        """
        if 'Close' not in data.columns:
            raise ValueError("DataFrame must contain 'Close' column")
        
        if period == "daily":
            return data['Close'].pct_change()
        elif period == "weekly":
            weekly_data = data['Close'].resample('W').last()
            return weekly_data.pct_change()
        elif period == "monthly":
            monthly_data = data['Close'].resample('M').last()
            return monthly_data.pct_change()
        else:
            raise ValueError("Period must be 'daily', 'weekly', or 'monthly'")
    
    def get_moving_averages(self, data: pd.DataFrame, windows: List[int] = [20, 50, 200]) -> pd.DataFrame:
        """
        Calculate moving averages for stock data.
        
        Args:
            data: DataFrame with price data (must have 'Close' column)
            windows: List of window sizes for moving averages
            
        Returns:
            DataFrame with original data and moving averages
        """
        if 'Close' not in data.columns:
            raise ValueError("DataFrame must contain 'Close' column")
        
        result = data.copy()
        for window in windows:
            result[f'MA_{window}'] = data['Close'].rolling(window=window).mean()
        
        return result
    
    def get_volatility(self, data: pd.DataFrame, window: int = 30) -> pd.Series:
        """
        Calculate rolling volatility (standard deviation of returns).
        
        Args:
            data: DataFrame with price data (must have 'Close' column)
            window: Rolling window size
            
        Returns:
            Series with rolling volatility
        """
        returns = self.calculate_returns(data, "daily")
        return returns.rolling(window=window).std() * (252 ** 0.5)  # Annualized volatility
