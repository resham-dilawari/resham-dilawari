"""
Risk Assessment Agent
Specializes in portfolio risk, diversification, volatility, and risk-adjusted returns
"""
from typing import Dict, Any, List
from .base_agent import BaseAgent


class RiskAssessmentAgent(BaseAgent):
    """Agent specialized in risk analysis and portfolio risk management."""
    
    def __init__(self):
        super().__init__(
            agent_name="Risk Assessment Agent",
            specialization="portfolio risk, diversification analysis, volatility assessment, and risk-adjusted returns"
        )
        
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze risk profile of a stock or portfolio.
        
        Expected context:
        - ticker: Stock ticker (for single stock) or "Portfolio" for overall
        - beta: Stock beta vs. market
        - volatility: Historical volatility
        - max_drawdown: Maximum historical drawdown
        - var: Value at Risk
        - sharpe_ratio: Risk-adjusted return metric
        - correlation_matrix: Correlations with other holdings
        """
        self.log_action("start_risk_analysis", {"ticker": context.get("ticker")})
        
        prompt = f"""{self.get_system_prompt()}

Perform comprehensive risk analysis:

Asset: {context.get('ticker', 'N/A')}
Beta: {context.get('beta', 'N/A')} (Market = 1.0)
Historical Volatility (Annual): {context.get('volatility', 'N/A')}%
Maximum Drawdown: {context.get('max_drawdown', 'N/A')}%
Sharpe Ratio: {context.get('sharpe_ratio', 'N/A')}
Value at Risk (95%): {context.get('var_95', 'N/A')}
Downside Deviation: {context.get('downside_deviation', 'N/A')}
Correlation with NIFTY50: {context.get('market_correlation', 'N/A')}

User Risk Profile: {context.get('user_risk_profile', 'Moderate')}

Provide detailed risk assessment:
1. Risk Level Classification (Very High/High/Moderate/Low/Very Low)
2. Volatility analysis and what it means for investor
3. Downside risk assessment
4. Beta interpretation (systematic risk exposure)
5. Maximum potential loss scenarios
6. Risk-adjusted return quality (Sharpe ratio analysis)
7. Suitability for different investor types
8. Risk mitigation strategies

Provide risk rating: VERY HIGH RISK / HIGH RISK / MODERATE RISK / LOW RISK / VERY LOW RISK
Include confidence level and key risk factors.
"""
        
        analysis_text = self.generate_response(prompt, temperature=0.3)
        
        result = {
            "agent": self.agent_name,
            "ticker": context.get("ticker"),
            "analysis": analysis_text,
            "timestamp": self.execution_log[-1]["timestamp"] if self.execution_log else None,
            "type": "risk_analysis"
        }
        
        self.log_action("complete_risk_analysis", {"ticker": context.get("ticker")})
        
        return result
    
    def portfolio_diversification_check(self, portfolio: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze portfolio diversification and concentration risks."""
        self.log_action("diversification_analysis", {"holdings": len(portfolio)})
        
        holdings_summary = "\n".join([
            f"- {holding.get('ticker')}: {holding.get('weight', 0)}% allocation, "
            f"Sector: {holding.get('sector', 'N/A')}, Beta: {holding.get('beta', 'N/A')}"
            for holding in portfolio
        ])
        
        prompt = f"""{self.get_system_prompt()}

Analyze diversification of the following portfolio:

Holdings:
{holdings_summary}

Total Holdings: {len(portfolio)}

Assess:
1. Diversification score (1-10, 10 being perfectly diversified)
2. Sector concentration risks
3. Geographic concentration (if applicable)
4. Correlation analysis among holdings
5. Systematic vs. idiosyncratic risk balance
6. Over-diversification or under-diversification issues
7. Specific recommendations to improve diversification

Provide clear actionable recommendations for portfolio balance.
"""
        
        analysis_text = self.generate_response(prompt, temperature=0.4)
        
        return {
            "agent": self.agent_name,
            "analysis": analysis_text,
            "type": "diversification_analysis",
            "holdings_count": len(portfolio)
        }
    
    def stress_test(self, portfolio: List[Dict[str, Any]], scenario: str) -> Dict[str, Any]:
        """Run stress test scenarios on portfolio."""
        self.log_action("stress_test", {"scenario": scenario})
        
        holdings_summary = "\n".join([
            f"- {holding.get('ticker')}: ₹{holding.get('value', 0):,.0f}, "
            f"Beta: {holding.get('beta', 1.0)}"
            for holding in portfolio
        ])
        
        scenarios_map = {
            "market_crash": "Market crashes 30% (like 2008 or March 2020)",
            "rate_hike": "RBI hikes rates by 200 basis points aggressively",
            "recession": "Indian economy enters recession, GDP contracts 5%",
            "sector_crash": "Specific sector faces regulatory crackdown"
        }
        
        scenario_desc = scenarios_map.get(scenario, scenario)
        
        prompt = f"""{self.get_system_prompt()}

Perform stress test on portfolio under scenario: {scenario_desc}

Portfolio Holdings:
{holdings_summary}

Total Portfolio Value: ₹{sum([h.get('value', 0) for h in portfolio]):,.0f}

Estimate:
1. Potential portfolio loss (% and absolute ₹)
2. Which holdings would be most impacted
3. Which holdings might provide stability/hedge
4. Recovery timeline estimate
5. Actions to take before/during such scenario
6. Portfolio resilience score (1-10)

Provide stress test results with confidence intervals.
"""
        
        stress_analysis = self.generate_response(prompt, temperature=0.4)
        
        return {
            "agent": self.agent_name,
            "analysis": stress_analysis,
            "type": "stress_test",
            "scenario": scenario
        }
