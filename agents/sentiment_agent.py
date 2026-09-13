"""
News Sentiment Agent
Specializes in analyzing news, social media, and market sentiment
"""
from typing import Dict, Any, List
from .base_agent import BaseAgent


class SentimentAnalysisAgent(BaseAgent):
    """Agent specialized in news sentiment and market psychology analysis."""
    
    def __init__(self):
        super().__init__(
            agent_name="News Sentiment Agent",
            specialization="news analysis, market sentiment, social signals, and narrative tracking"
        )
        
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze news sentiment and market psychology.
        
        Expected context:
        - ticker: Stock ticker symbol
        - news_headlines: List of recent news headlines
        - news_publishers: Sources of news
        - social_mentions: Social media activity (if available)
        """
        self.log_action("start_sentiment_analysis", {"ticker": context.get("ticker")})
        
        news_data = context.get("news_headlines", [])
        if isinstance(news_data, str):
            news_text = news_data
        else:
            news_text = "\n".join([f"- {item}" for item in news_data])
        
        prompt = f"""{self.get_system_prompt()}

Analyze the sentiment and narrative around the following stock:

Ticker: {context.get('ticker', 'N/A')}
Recent News:
{news_text}

Social Media Mentions: {context.get('social_mentions', 'N/A')}
Analyst Ratings: {context.get('analyst_ratings', 'N/A')}

Provide comprehensive sentiment analysis:
1. Overall Sentiment (Bullish/Bearish/Neutral) with confidence score
2. Key narrative themes and storylines
3. Sentiment drivers (positive and negative)
4. News quality and credibility assessment
5. Comparison: Market sentiment vs. actual fundamentals
6. Potential sentiment shifts and catalysts to watch
7. Herd behavior or contrarian opportunity indicators

Rate the sentiment impact: VERY POSITIVE / POSITIVE / NEUTRAL / NEGATIVE / VERY NEGATIVE
Assess whether current sentiment is warranted or overblown.
"""
        
        analysis_text = self.generate_response(prompt, temperature=0.5)
        
        result = {
            "agent": self.agent_name,
            "ticker": context.get("ticker"),
            "analysis": analysis_text,
            "timestamp": self.execution_log[-1]["timestamp"] if self.execution_log else None,
            "type": "sentiment_analysis"
        }
        
        self.log_action("complete_sentiment_analysis", {
            "ticker": context.get("ticker"),
            "news_items_analyzed": len(news_data) if isinstance(news_data, list) else "unknown"
        })
        
        return result
    
    def detect_market_narratives(self, multi_stock_news: Dict[str, List[str]]) -> Dict[str, Any]:
        """Detect broader market narratives across multiple stocks."""
        self.log_action("narrative_detection", {"stocks_count": len(multi_stock_news)})
        
        combined_news = "\n\n".join([
            f"{ticker}:\n" + "\n".join(headlines)
            for ticker, headlines in multi_stock_news.items()
        ])
        
        prompt = f"""{self.get_system_prompt()}

Analyze the following news across multiple stocks to detect broader market narratives:

{combined_news}

Identify:
1. Common themes across companies (sector trends, macro factors)
2. Emerging market narratives
3. Risk-off vs. risk-on sentiment
4. Sector rotation signals
5. Potential Black Swan events or tail risks

Provide strategic insights for portfolio positioning.
"""
        
        narrative_analysis = self.generate_response(prompt, temperature=0.6)
        
        return {
            "agent": self.agent_name,
            "analysis": narrative_analysis,
            "type": "market_narrative",
            "stocks_analyzed": list(multi_stock_news.keys())
        }
    
    def contrarian_check(self, ticker: str, sentiment_score: str, price_action: str) -> Dict[str, Any]:
        """Check for contrarian opportunities (sentiment vs. price divergence)."""
        prompt = f"""{self.get_system_prompt()}

Contrarian Analysis for {ticker}:
Current Sentiment: {sentiment_score}
Recent Price Action: {price_action}

Identify:
1. Is there a divergence between sentiment and price?
2. Potential contrarian opportunity or value trap?
3. Historical examples of similar situations
4. Risk/reward assessment for contrarian position

Recommend: CONTRARIAN BUY / WAIT / AVOID
"""
        
        analysis = self.generate_response(prompt, temperature=0.5)
        
        return {
            "agent": self.agent_name,
            "ticker": ticker,
            "analysis": analysis,
            "type": "contrarian_analysis"
        }
