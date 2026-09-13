import yfinance as yf
import pandas as pd

def get_stock_info(ticker: str) -> str:
    """Fetches the business summary for a given ticker."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        if "longBusinessSummary" in info:
            return info["longBusinessSummary"]
        elif "description" in info:
            return info["description"]
        else:
            return f"No business summary available for {ticker}."
    except Exception as e:
        return f"Error fetching info for {ticker}: {e}"

def get_recent_news(ticker: str) -> str:
    """Fetches recent news headlines for a given ticker."""
    try:
        stock = yf.Ticker(ticker)
        news_items = stock.news
        if not news_items:
            return f"No recent news found for {ticker}."
        
        headlines = []
        for item in news_items[:5]:  # Get top 5 news items
            title = item.get("title", "No Title")
            publisher = item.get("publisher", "Unknown Publisher")
            headlines.append(f"- {title} (Source: {publisher})")
            
        return "\n".join(headlines)
    except Exception as e:
        return f"Error fetching news for {ticker}: {e}"

def get_current_price(ticker: str) -> str:
    """Fetches the current price and previous close."""
    try:
        stock = yf.Ticker(ticker)
        fast_info = stock.fast_info
        last_price = fast_info.last_price
        prev_close = fast_info.previous_close
        
        change = last_price - prev_close
        pct_change = (change / prev_close) * 100
        
        return f"Current Price: {last_price:.2f}, Change: {change:.2f} ({pct_change:.2f}%)"
    except Exception as e:
        return f"Error fetching price for {ticker}: {e}"

def get_full_stock_profile(ticker: str) -> str:
    """Aggregates all info into a single string for the LLM."""
    ticker = ticker.strip().upper()
    profile = f"--- Data for {ticker} ---\n"
    profile += f"{get_current_price(ticker)}\n\n"
    profile += "Business Summary:\n"
    profile += f"{get_stock_info(ticker)}\n\n"
    profile += "Recent News:\n"
    profile += f"{get_recent_news(ticker)}\n"
    profile += "-" * 30 + "\n"
    return profile
