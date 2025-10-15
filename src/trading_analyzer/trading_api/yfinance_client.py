"""YFinance client for stock data retrieval and analysis."""

from typing import Any, Dict, List, Optional

import pandas as pd
import yfinance as yf


class YFinanceClient:
    """Yahoo Finance API client for stock data and analysis."""

    def __init__(self):
        """Initialize the YFinance client."""
        pass

    def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        """Get basic stock information."""
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
        interval: str = "1d",
    ) -> pd.DataFrame:
        """Get historical stock data."""
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
        end: Optional[str] = None,
    ) -> Dict[str, pd.DataFrame]:
        """Get historical data for multiple stocks."""
        results = {}
        for symbol in symbols:
            try:
                results[symbol] = self.get_historical_data(symbol, period, start, end)
            except Exception as e:
                print(f"Warning: Could not fetch data for {symbol}: {str(e)}")
                results[symbol] = pd.DataFrame()

        return results

    def get_current_price(self, symbol: str) -> float:
        """Get current stock price."""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d", interval="1m")
            if data.empty:
                # Fallback to daily data
                data = ticker.history(period="1d")

            if data.empty:
                raise Exception(f"No current price data available for {symbol}")

            return float(data["Close"].iloc[-1])
        except Exception as e:
            raise Exception(f"Error fetching current price for {symbol}: {str(e)}")

    def get_dividends(self, symbol: str) -> pd.DataFrame:
        """Get dividend history."""
        try:
            ticker = yf.Ticker(symbol)
            dividends = ticker.dividends
            return (
                dividends.to_frame("Dividend")
                if not dividends.empty
                else pd.DataFrame()
            )
        except Exception as e:
            raise Exception(f"Error fetching dividends for {symbol}: {str(e)}")

    def get_splits(self, symbol: str) -> pd.DataFrame:
        """Get stock split history."""
        try:
            ticker = yf.Ticker(symbol)
            splits = ticker.splits
            return splits.to_frame("Split") if not splits.empty else pd.DataFrame()
        except Exception as e:
            raise Exception(f"Error fetching splits for {symbol}: {str(e)}")

    def calculate_returns(self, data: pd.DataFrame, period: str = "daily") -> pd.Series:
        """Calculate returns from price data."""
        if "Close" not in data.columns:
            raise ValueError("DataFrame must contain 'Close' column")

        if period == "daily":
            return data["Close"].pct_change()
        elif period == "weekly":
            weekly_data = data["Close"].resample("W").last()
            return weekly_data.pct_change()
        elif period == "monthly":
            monthly_data = data["Close"].resample("M").last()
            return monthly_data.pct_change()
        else:
            raise ValueError("Period must be 'daily', 'weekly', or 'monthly'")

    def get_moving_averages(
        self, data: pd.DataFrame, windows: List[int] = [20, 50, 200]
    ) -> pd.DataFrame:
        """Calculate moving averages."""
        if "Close" not in data.columns:
            raise ValueError("DataFrame must contain 'Close' column")

        result = data.copy()
        for window in windows:
            result[f"MA_{window}"] = data["Close"].rolling(window=window).mean()

        return result

    def get_volatility(self, data: pd.DataFrame, window: int = 30) -> pd.Series:
        """Calculate rolling volatility."""
        returns = self.calculate_returns(data, "daily")
        return returns.rolling(window=window).std() * (
            252**0.5
        )  # Annualized volatility
