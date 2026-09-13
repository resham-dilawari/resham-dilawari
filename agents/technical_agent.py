"""
Technical Analysis Agent
Specializes in price patterns, trends, momentum indicators, and trading signals
"""
from typing import Dict, Any, List
from .base_agent import BaseAgent
import json


class TechnicalAnalysisAgent(BaseAgent):
    """Agent specialized in technical analysis and chart patterns."""
    
    def __init__(self):
        super().__init__(
            agent_name="Technical Analysis Agent",
            specialization="price patterns, trend analysis, momentum indicators, and trading signals"
        )
        
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform technical analysis on stock data.
        
        Expected context:
        - ticker: Stock ticker symbol
        - price_history: Historical price data
        - volume_data: Trading volume information
        - moving_averages: MA50, MA200, etc.
        - rsi: Relative Strength Index
        - macd: MACD indicator values
        """
        self.log_action("start_technical_analysis", {"ticker": context.get("ticker")})
        
        prompt = f"""{self.get_system_prompt()}

Perform technical analysis on the following stock:

Ticker: {context.get('ticker', 'N/A')}
Current Price: ₹{context.get('current_price', 'N/A')}
Price Change Today: {context.get('price_change_pct', 'N/A')}%
52-Week High: ₹{context.get('week_52_high', 'N/A')}
52-Week Low: ₹{context.get('week_52_low', 'N/A')}
50-Day MA: ₹{context.get('ma_50', 'N/A')}
200-Day MA: ₹{context.get('ma_200', 'N/A')}
RSI (14): {context.get('rsi', 'N/A')}
MACD: {context.get('macd', 'N/A')}
Average Volume: {context.get('avg_volume', 'N/A')}
Current Volume: {context.get('current_volume', 'N/A')}

Recent Price Action: {context.get('recent_price_action', 'N/A')}

Provide comprehensive technical analysis including:
1. Trend identification (Uptrend/Downtrend/Sideways)
2. Support and resistance levels
3. Momentum indicators interpretation (RSI, MACD)
4. Volume analysis and accumulation/distribution patterns
5. Key chart patterns (if any)
6. Entry and exit points for traders
7. Short-term (1-2 weeks) and medium-term (1-3 months) outlook

Provide a technical rating: STRONG BUY / BUY / HOLD / SELL / STRONG SELL
Include confidence level and key technical triggers to watch.
"""
        
        analysis_text = self.generate_response(prompt, temperature=0.3)
        
        result = {
            "agent": self.agent_name,
            "ticker": context.get("ticker"),
            "analysis": analysis_text,
            "timestamp": self.execution_log[-1]["timestamp"] if self.execution_log else None,
            "type": "technical_analysis"
        }
        
        self.log_action("complete_technical_analysis", {
            "ticker": context.get("ticker"),
            "success": True
        })
        
        return result
    
    def identify_patterns(self, price_data: List[float], ticker: str) -> Dict[str, Any]:
        """Identify chart patterns in price data."""
        self.log_action("pattern_recognition", {"ticker": ticker})
        
        # Simple pattern recognition based on recent price movements
        if len(price_data) < 5:
            return {
                "agent": self.agent_name,
                "patterns": "Insufficient data for pattern recognition",
                "ticker": ticker
            }
        
        recent_prices = price_data[-10:]
        price_summary = f"Recent prices: {', '.join([f'₹{p:.2f}' for p in recent_prices])}"
        
        prompt = f"""{self.get_system_prompt()}

Analyze the following price sequence for {ticker} and identify any chart patterns:

{price_summary}

Identify patterns such as:
- Head and Shoulders
- Double Top/Bottom
- Triangles (Ascending, Descending, Symmetrical)
- Flags and Pennants
- Cup and Handle
- Breakout patterns

Provide pattern name, reliability, and trading implications.
"""
        
        pattern_analysis = self.generate_response(prompt, temperature=0.3)
        
        return {
            "agent": self.agent_name,
            "ticker": ticker,
            "patterns": pattern_analysis,
            "type": "pattern_recognition"
        }
