from langchain.tools import BaseTool
import yfinance as yf
from typing import Optional
import datetime

class StockPriceTool(BaseTool):
    name: str = "get_stock_price"
    description: str = "Get the current or historical stock price for a given ticker symbol"
    
    def _run(self, ticker: str) -> dict:
        """Get the latest stock information for the specified ticker."""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            end_date = datetime.datetime.now()
            start_date = end_date - datetime.timedelta(days=30)
            history = stock.history(start=start_date, end=end_date)
            
            if not history.empty:
                current_price = history['Close'].iloc[-1]
                avg_price = history['Close'].mean()
                high_30d = history['High'].max()
                low_30d = history['Low'].min()
                
                return {
                    "ticker": ticker,
                    "name": info.get('shortName', ticker),
                    "current_price": current_price,
                    "currency": info.get('currency', 'USD'),
                    "previous_close": info.get('previousClose'),
                    "market_cap": info.get('marketCap'),
                    "52wk_high": info.get('fiftyTwoWeekHigh'),
                    "52wk_low": info.get('fiftyTwoWeekLow'),
                    "30d_avg_price": avg_price,
                    "30d_high": high_30d,
                    "30d_low": low_30d,
                    "pe_ratio": info.get('trailingPE'),
                    "dividend_yield": info.get('dividendYield'),
                    "volume": info.get('volume'),
                    "timestamp": datetime.datetime.now().isoformat()
                }
            else:
                return {"error": f"No data available for ticker {ticker}"}
                
        except Exception as e:
            return {"error": f"Error fetching stock data: {str(e)}"}
    
    def _arun(self, ticker: str):
        """Async implementation of the tool."""
        return self._run(ticker)
