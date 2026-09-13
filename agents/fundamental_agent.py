"""
Fundamental Analysis Agent
Specializes in company financials, valuation, and business model analysis
"""
from typing import Dict, Any
from .base_agent import BaseAgent
import json


class FundamentalAnalysisAgent(BaseAgent):
    """Agent specialized in fundamental analysis of stocks."""
    
    def __init__(self):
        super().__init__(
            agent_name="Fundamental Analysis Agent",
            specialization="company financials, business models, valuation metrics, and growth prospects"
        )
        
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform fundamental analysis on stock data.
        
        Expected context:
        - ticker: Stock ticker symbol
        - business_summary: Company description
        - financial_metrics: P/E, P/B, Debt-to-Equity, ROE, etc.
        - price_data: Current price, historical performance
        """
        self.log_action("start_analysis", {"ticker": context.get("ticker")})
        
        prompt = f"""{self.get_system_prompt()}

Analyze the following company from a fundamental perspective:

Ticker: {context.get('ticker', 'N/A')}
Business Summary: {context.get('business_summary', 'N/A')}
Current Price: {context.get('current_price', 'N/A')}
Market Cap: {context.get('market_cap', 'N/A')}
P/E Ratio: {context.get('pe_ratio', 'N/A')}
P/B Ratio: {context.get('pb_ratio', 'N/A')}
Dividend Yield: {context.get('dividend_yield', 'N/A')}
ROE: {context.get('roe', 'N/A')}
Debt to Equity: {context.get('debt_to_equity', 'N/A')}
Profit Margin: {context.get('profit_margin', 'N/A')}
Revenue Growth: {context.get('revenue_growth', 'N/A')}

Provide a comprehensive fundamental analysis including:
1. Business model strength and competitive moat
2. Valuation assessment (fairly valued, overvalued, undervalued)
3. Financial health and quality of earnings
4. Growth prospects and sustainability
5. Management quality indicators
6. Industry position and competitive advantages

Rate the fundamental strength as: STRONG BUY / BUY / HOLD / SELL / STRONG SELL
Include your confidence level and key assumptions.
"""
        
        analysis_text = self.generate_response(prompt, temperature=0.4)
        
        result = {
            "agent": self.agent_name,
            "ticker": context.get("ticker"),
            "analysis": analysis_text,
            "timestamp": self.execution_log[-1]["timestamp"] if self.execution_log else None,
            "type": "fundamental_analysis"
        }
        
        self.log_action("complete_analysis", {"ticker": context.get("ticker"), "success": True})
        
        return result
    
    def compare_peers(self, companies: list[Dict[str, Any]]) -> Dict[str, Any]:
        """Compare multiple companies for relative valuation."""
        self.log_action("peer_comparison", {"count": len(companies)})
        
        comparison_data = "\n\n".join([
            f"Company: {c.get('ticker')}\nP/E: {c.get('pe_ratio')}\nROE: {c.get('roe')}\n"
            f"Revenue Growth: {c.get('revenue_growth')}\nDebt/Equity: {c.get('debt_to_equity')}"
            for c in companies
        ])
        
        prompt = f"""{self.get_system_prompt()}

Compare the following companies from a fundamental perspective:

{comparison_data}

Provide:
1. Relative valuation analysis
2. Best value pick and why
3. Strongest business model
4. Risk comparison across companies
"""
        
        comparison_text = self.generate_response(prompt, temperature=0.4)
        
        return {
            "agent": self.agent_name,
            "analysis": comparison_text,
            "type": "peer_comparison",
            "companies_analyzed": len(companies)
        }
