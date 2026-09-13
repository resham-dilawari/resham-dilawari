"""
Portfolio Optimizer Agent
Specializes in asset allocation, rebalancing, and portfolio optimization
"""
from typing import Dict, Any, List
from .base_agent import BaseAgent


class PortfolioOptimizerAgent(BaseAgent):
    """Agent specialized in portfolio optimization and asset allocation."""
    
    def __init__(self):
        super().__init__(
            agent_name="Portfolio Optimizer Agent",
            specialization="asset allocation, portfolio optimization, rebalancing strategies, and efficient frontier analysis"
        )
        
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize portfolio allocation.
        
        Expected context:
        - current_portfolio: List of current holdings with weights
        - investment_goals: User's financial goals
        - risk_tolerance: Conservative/Moderate/Aggressive
        - time_horizon: Investment timeframe
        - constraints: Any investment constraints
        """
        self.log_action("start_optimization", {
            "risk_tolerance": context.get("risk_tolerance")
        })
        
        current_holdings = context.get("current_portfolio", [])
        holdings_summary = "\n".join([
            f"- {h.get('ticker')}: ₹{h.get('value', 0):,.0f} ({h.get('weight', 0):.1f}%), "
            f"Return: {h.get('return', 0):.1f}%"
            for h in current_holdings
        ])
        
        prompt = f"""{self.get_system_prompt()}

Optimize the following portfolio:

Current Holdings:
{holdings_summary}

Total Portfolio Value: ₹{context.get('total_value', 0):,.0f}
Available Cash to Invest: ₹{context.get('available_cash', 0):,.0f}

User Profile:
- Risk Tolerance: {context.get('risk_tolerance', 'Moderate')}
- Time Horizon: {context.get('time_horizon', '5-10 years')}
- Investment Goals: {context.get('investment_goals', 'Wealth creation')}
- Age: {context.get('age', 'N/A')}
- Monthly Income: ₹{context.get('monthly_income', 'N/A'):,}

Constraints:
{context.get('constraints', 'None specified')}

Provide comprehensive portfolio optimization:
1. Optimal asset allocation recommendation (% breakdown)
2. Rebalancing suggestions (what to buy/sell)
3. New stock recommendations with allocation percentages
4. Sector allocation targets
5. Cash reserve recommendation
6. Expected portfolio metrics (return, volatility, Sharpe ratio)
7. Comparison: Current vs. Optimized portfolio

Provide specific actionable steps: "Sell X shares of ABC", "Buy Y shares of XYZ", etc.
"""
        
        analysis_text = self.generate_response(prompt, temperature=0.5)
        
        result = {
            "agent": self.agent_name,
            "analysis": analysis_text,
            "timestamp": self.execution_log[-1]["timestamp"] if self.execution_log else None,
            "type": "portfolio_optimization"
        }
        
        self.log_action("complete_optimization", {"success": True})
        
        return result
    
    def rebalancing_strategy(self, portfolio: List[Dict[str, Any]], target_allocation: Dict[str, float]) -> Dict[str, Any]:
        """Generate specific rebalancing recommendations."""
        self.log_action("rebalancing", {"holdings": len(portfolio)})
        
        current_allocation = "\n".join([
            f"- {h.get('ticker')}: Current {h.get('weight', 0):.1f}%"
            for h in portfolio
        ])
        
        target_summary = "\n".join([
            f"- {ticker}: Target {weight:.1f}%"
            for ticker, weight in target_allocation.items()
        ])
        
        prompt = f"""{self.get_system_prompt()}

Generate rebalancing plan:

Current Allocation:
{current_allocation}

Target Allocation:
{target_summary}

Total Portfolio Value: ₹{sum([h.get('value', 0) for h in portfolio]):,.0f}

Provide:
1. Specific buy/sell orders with quantities
2. Order execution sequence for tax efficiency
3. Transaction cost estimates
4. Optimal timing for rebalancing
5. Alternative approaches (threshold-based vs. calendar-based)
6. Tax implications of rebalancing

Make recommendations practical and executable.
"""
        
        rebalancing_plan = self.generate_response(prompt, temperature=0.4)
        
        return {
            "agent": self.agent_name,
            "analysis": rebalancing_plan,
            "type": "rebalancing_strategy"
        }
    
    def goal_based_allocation(self, goals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create goal-based portfolio allocation strategy."""
        self.log_action("goal_based_planning", {"goals": len(goals)})
        
        goals_summary = "\n".join([
            f"- {goal.get('name')}: ₹{goal.get('target_amount', 0):,}, "
            f"Timeline: {goal.get('years', 0)} years, "
            f"Priority: {goal.get('priority', 'Medium')}"
            for goal in goals
        ])
        
        prompt = f"""{self.get_system_prompt()}

Create goal-based investment strategy:

Financial Goals:
{goals_summary}

For each goal, recommend:
1. Appropriate asset allocation (equity/debt/gold ratio)
2. Specific investment products (stocks, mutual funds, ETFs)
3. Required monthly SIP amount
4. Risk level appropriate for timeline
5. Milestone checkpoints
6. Contingency plans if goals are off-track

Provide a holistic strategy connecting all goals.
"""
        
        strategy = self.generate_response(prompt, temperature=0.5)
        
        return {
            "agent": self.agent_name,
            "analysis": strategy,
            "type": "goal_based_allocation",
            "goals_count": len(goals)
        }
