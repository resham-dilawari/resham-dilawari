"""
Enhanced Financial Data Module for Multi-Agent System
Provides comprehensive data for all specialized agents
"""
import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import streamlit as st



class FinancialDataProvider:
    """Enhanced financial data provider with comprehensive metrics."""
    
    @staticmethod
    @st.cache_data(ttl=300, show_spinner=False)
    def get_comprehensive_stock_data(ticker: str) -> Dict[str, Any]:

        """
        Fetch comprehensive stock data for multi-agent analysis.
        
        Returns data structured for different agents:
        - Fundamental data
        - Technical indicators
        - News and sentiment data
        - Risk metrics
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="1y")
            
            if hist.empty:
                return {"error": f"No data available for {ticker}"}
            
            data = {
                "ticker": ticker,
                "timestamp": datetime.now().isoformat(),
                
                # Basic Info
                "company_name": info.get("longName", ticker),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                
                # Price Data
                "current_price": info.get("currentPrice", hist['Close'].iloc[-1]),
                "previous_close": info.get("previousClose", hist['Close'].iloc[-2] if len(hist) > 1 else None),
                "open": info.get("open", hist['Open'].iloc[-1]),
                "day_high": info.get("dayHigh", hist['High'].iloc[-1]),
                "day_low": info.get("dayLow", hist['Low'].iloc[-1]),
                
                # Fundamental Metrics
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "forward_pe": info.get("forwardPE"),
                "pb_ratio": info.get("priceToBook"),
                "ps_ratio": info.get("priceToSalesTrailing12Months"),
                "peg_ratio": info.get("pegRatio"),
                "dividend_yield": info.get("dividendYield"),
                "roe": info.get("returnOnEquity"),
                "roa": info.get("returnOnAssets"),
                "debt_to_equity": info.get("debtToEquity"),
                "current_ratio": info.get("currentRatio"),
                "profit_margin": info.get("profitMargins"),
                "operating_margin": info.get("operatingMargins"),
                "revenue_growth": info.get("revenueGrowth"),
                "earnings_growth": info.get("earningsGrowth"),
                "free_cash_flow": info.get("freeCashflow"),
                
                # Business Info
                "business_summary": info.get("longBusinessSummary", "N/A"),
                
                # Technical Metrics
                "week_52_high": info.get("fiftyTwoWeekHigh"),
                "week_52_low": info.get("fiftyTwoWeekLow"),
                "ma_50": info.get("fiftyDayAverage"),
                "ma_200": info.get("twoHundredDayAverage"),
                "avg_volume": info.get("averageVolume"),
                "volume": info.get("volume"),
                
                # Risk Metrics
                "beta": info.get("beta"),
                
                # Analyst Data
                "target_price": info.get("targetMeanPrice"),
                "recommendation": info.get("recommendationKey"),
                "number_of_analysts": info.get("numberOfAnalystOpinions"),
            }
            
            # Calculate additional technical indicators
            data.update(FinancialDataProvider._calculate_technical_indicators(hist))
            
            # Calculate risk metrics
            data.update(FinancialDataProvider._calculate_risk_metrics(hist))
            
            # Get news
            data["news"] = FinancialDataProvider._get_news(stock)
            
            # Price change calculations
            if data["current_price"] and data["previous_close"]:
                change = data["current_price"] - data["previous_close"]
                data["price_change"] = change
                data["price_change_pct"] = (change / data["previous_close"]) * 100
            
            return data
            
        except Exception as e:
            return {"error": f"Error fetching data for {ticker}: {str(e)}"}
    
    @staticmethod
    def _calculate_technical_indicators(hist: pd.DataFrame) -> Dict[str, Any]:
        """Calculate technical indicators from price history."""
        if hist.empty or len(hist) < 20:
            return {}
        
        close_prices = hist['Close']
        
        indicators = {}
        
        # RSI (14-day)
        try:
            delta = close_prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            indicators["rsi"] = round(rsi.iloc[-1], 2) if not pd.isna(rsi.iloc[-1]) else None
        except:
            indicators["rsi"] = None
        
        # MACD
        try:
            ema_12 = close_prices.ewm(span=12, adjust=False).mean()
            ema_26 = close_prices.ewm(span=26, adjust=False).mean()
            macd = ema_12 - ema_26
            signal = macd.ewm(span=9, adjust=False).mean()
            indicators["macd"] = round(macd.iloc[-1], 2) if not pd.isna(macd.iloc[-1]) else None
            indicators["macd_signal"] = round(signal.iloc[-1], 2) if not pd.isna(signal.iloc[-1]) else None
        except:
            indicators["macd"] = None
            indicators["macd_signal"] = None
        
        # Moving Averages
        try:
            indicators["sma_20"] = round(close_prices.rolling(window=20).mean().iloc[-1], 2)
            indicators["sma_50"] = round(close_prices.rolling(window=50).mean().iloc[-1], 2)
            if len(close_prices) >= 200:
                indicators["sma_200"] = round(close_prices.rolling(window=200).mean().iloc[-1], 2)
        except:
            pass
        
        # Recent price action summary
        try:
            recent_prices = close_prices.tail(10).tolist()
            indicators["recent_price_action"] = ", ".join([f"₹{p:.2f}" for p in recent_prices])
        except:
            indicators["recent_price_action"] = "N/A"
        
        return indicators
    
    @staticmethod
    def _calculate_risk_metrics(hist: pd.DataFrame) -> Dict[str, Any]:
        """Calculate risk metrics from price history."""
        if hist.empty or len(hist) < 20:
            return {}
        
        close_prices = hist['Close']
        returns = close_prices.pct_change().dropna()
        
        metrics = {}
        
        # Volatility (annualized)
        try:
            daily_vol = returns.std()
            metrics["volatility"] = round(daily_vol * np.sqrt(252) * 100, 2)  # Annualized %
        except:
            metrics["volatility"] = None
        
        # Maximum Drawdown
        try:
            cumulative = (1 + returns).cumprod()
            running_max = cumulative.cummax()
            drawdown = (cumulative - running_max) / running_max
            metrics["max_drawdown"] = round(drawdown.min() * 100, 2)  # Percentage
        except:
            metrics["max_drawdown"] = None
        
        # Sharpe Ratio (assuming 6% risk-free rate for India)
        try:
            risk_free_rate = 0.06
            excess_returns = returns.mean() * 252 - risk_free_rate
            sharpe = excess_returns / (returns.std() * np.sqrt(252))
            metrics["sharpe_ratio"] = round(sharpe, 2)
        except:
            metrics["sharpe_ratio"] = None
        
        # Value at Risk (95% confidence)
        try:
            var_95 = np.percentile(returns, 5)
            metrics["var_95"] = round(var_95 * 100, 2)  # Daily VaR in %
        except:
            metrics["var_95"] = None
        
        # Downside Deviation
        try:
            downside_returns = returns[returns < 0]
            metrics["downside_deviation"] = round(downside_returns.std() * np.sqrt(252) * 100, 2)
        except:
            metrics["downside_deviation"] = None
        
        return metrics
    
    @staticmethod
    def _get_news(stock) -> List[Dict[str, str]]:
        """Get recent news headlines."""
        try:
            news_items = stock.news
            if not news_items:
                return []
            
            news_list = []
            for item in news_items[:10]:  # Top 10 news items
                news_list.append({
                    "title": item.get("title", "No Title"),
                    "publisher": item.get("publisher", "Unknown"),
                    "link": item.get("link", ""),
                    "published": item.get("providerPublishTime", "")
                })
            return news_list
        except:
            return []
    
    @staticmethod
    def get_portfolio_data(tickers: List[str]) -> List[Dict[str, Any]]:
        """Get comprehensive data for multiple stocks — fetched in parallel."""
        if not tickers:
            return []

        results: Dict[str, Dict[str, Any]] = {}

        with ThreadPoolExecutor(max_workers=min(len(tickers), 8)) as executor:
            future_to_ticker = {
                executor.submit(
                    FinancialDataProvider.get_comprehensive_stock_data, ticker
                ): ticker
                for ticker in tickers
            }
            for future in as_completed(future_to_ticker):
                ticker = future_to_ticker[future]
                try:
                    data = future.result()
                    if "error" not in data:
                        results[ticker] = data
                except Exception as e:
                    pass  # Skip tickers that fail; error is already handled inside

        # Return in original ticker order
        return [results[t] for t in tickers if t in results]

    
    @staticmethod
    def format_for_agents(stock_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """
        Format comprehensive stock data for different agents.
        Returns a dictionary with agent-specific data views.
        """
        return {
            "fundamental": {
                "ticker": stock_data.get("ticker"),
                "business_summary": stock_data.get("business_summary"),
                "current_price": stock_data.get("current_price"),
                "market_cap": stock_data.get("market_cap"),
                "pe_ratio": stock_data.get("pe_ratio"),
                "pb_ratio": stock_data.get("pb_ratio"),
                "dividend_yield": stock_data.get("dividend_yield"),
                "roe": stock_data.get("roe"),
                "debt_to_equity": stock_data.get("debt_to_equity"),
                "profit_margin": stock_data.get("profit_margin"),
                "revenue_growth": stock_data.get("revenue_growth"),
                "earnings_growth": stock_data.get("earnings_growth"),
            },
            "technical": {
                "ticker": stock_data.get("ticker"),
                "current_price": stock_data.get("current_price"),
                "price_change_pct": stock_data.get("price_change_pct"),
                "week_52_high": stock_data.get("week_52_high"),
                "week_52_low": stock_data.get("week_52_low"),
                "ma_50": stock_data.get("ma_50"),
                "ma_200": stock_data.get("ma_200"),
                "rsi": stock_data.get("rsi"),
                "macd": stock_data.get("macd"),
                "avg_volume": stock_data.get("avg_volume"),
                "current_volume": stock_data.get("volume"),
                "recent_price_action": stock_data.get("recent_price_action"),
            },
            "sentiment": {
                "ticker": stock_data.get("ticker"),
                "news_headlines": [n.get("title") for n in stock_data.get("news", [])],
                "analyst_ratings": stock_data.get("recommendation"),
                "target_price": stock_data.get("target_price"),
                "number_of_analysts": stock_data.get("number_of_analysts"),
            },
            "risk": {
                "ticker": stock_data.get("ticker"),
                "beta": stock_data.get("beta"),
                "volatility": stock_data.get("volatility"),
                "max_drawdown": stock_data.get("max_drawdown"),
                "sharpe_ratio": stock_data.get("sharpe_ratio"),
                "var_95": stock_data.get("var_95"),
                "downside_deviation": stock_data.get("downside_deviation"),
            }
        }
