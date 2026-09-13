"""
Tax Optimization Agent
Specializes in tax-efficient investing strategies for Indian tax regime
"""
from typing import Dict, Any, List
from .base_agent import BaseAgent


class TaxOptimizationAgent(BaseAgent):
    """Agent specialized in tax optimization for Indian investors."""
    
    def __init__(self):
        super().__init__(
            agent_name="Tax Optimization Agent",
            specialization="tax-efficient investing, STCG/LTCG optimization, tax-loss harvesting, and Section 80C strategies"
        )
        
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze tax implications and provide optimization strategies.
        
        Expected context:
        - holdings: List of holdings with purchase dates and prices
        - income_bracket: User's tax bracket
        - realized_gains: Gains already realized this FY
        - planned_redemptions: Upcoming sale plans
        """
        self.log_action("start_tax_analysis", {
            "holdings": len(context.get("holdings", []))
        })
        
        holdings_summary = "\n".join([
            f"- {h.get('ticker')}: Buy Date: {h.get('purchase_date')}, "
            f"Purchase Price: ₹{h.get('purchase_price', 0):.2f}, "
            f"Current Price: ₹{h.get('current_price', 0):.2f}, "
            f"Gain/Loss: ₹{h.get('unrealized_gain', 0):,.0f}"
            for h in context.get("holdings", [])
        ])
        
        prompt = f"""{self.get_system_prompt()}

Provide tax optimization analysis for Indian investor:

Holdings:
{holdings_summary}

User Profile:
- Income Tax Bracket: {context.get('income_bracket', '30%')}
- Realized Gains this FY: ₹{context.get('realized_gains', 0):,.0f}
- Unrealized Losses: ₹{context.get('unrealized_losses', 0):,.0f}
- Financial Year: {context.get('financial_year', 'FY 2026-27')}

Current Indian Tax Rules (as of 2026):
- LTCG (>1 year): 12.5% above ₹1.25 lakh exemption
- STCG (<1 year): 20%
- Dividend: Taxed at slab rate

Provide comprehensive tax strategy:
1. Identify holdings approaching LTCG status (hold a bit longer)
2. Tax-loss harvesting opportunities
3. Optimal timing for selling (STCG vs LTCG consideration)
4. Rebalancing strategies to minimize tax impact
5. Dividend-paying stocks vs growth stocks from tax perspective
6. Section 80C opportunities (ELSS funds, etc.)
7. Estimated tax liability for planned transactions
8. Year-end tax planning actions

Provide specific actionable tax-saving recommendations with estimated savings.
"""
        
        analysis_text = self.generate_response(prompt, temperature=0.3)
        
        result = {
            "agent": self.agent_name,
            "analysis": analysis_text,
            "timestamp": self.execution_log[-1]["timestamp"] if self.execution_log else None,
            "type": "tax_optimization"
        }
        
        self.log_action("complete_tax_analysis", {"success": True})
        
        return result
    
    def tax_loss_harvesting(self, losing_positions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Identify tax-loss harvesting opportunities."""
        self.log_action("tax_loss_harvesting", {"positions": len(losing_positions)})
        
        losses_summary = "\n".join([
            f"- {pos.get('ticker')}: Unrealized Loss: ₹{pos.get('loss', 0):,.0f}, "
            f"Holding Period: {pos.get('holding_days', 0)} days"
            for pos in losing_positions
        ])
        
        prompt = f"""{self.get_system_prompt()}

Identify tax-loss harvesting opportunities:

Losing Positions:
{losses_summary}

Recommendations needed:
1. Which losses to harvest now vs. later
2. Wash sale rule considerations (if applicable in India)
3. Replacement stocks to maintain market exposure
4. Timing optimization (before March 31 FY end)
5. Estimated tax savings
6. Impact on portfolio composition

Provide step-by-step execution plan.
"""
        
        harvesting_plan = self.generate_response(prompt, temperature=0.3)
        
        return {
            "agent": self.agent_name,
            "analysis": harvesting_plan,
            "type": "tax_loss_harvesting"
        }
    
    def year_end_planning(self, portfolio: List[Dict[str, Any]], tax_info: Dict[str, Any]) -> Dict[str, Any]:
        """Year-end tax planning strategies."""
        prompt = f"""{self.get_system_prompt()}

Year-end tax planning for FY {tax_info.get('financial_year', '2026-27')}:

Current Status:
- Realized LTCG: ₹{tax_info.get('realized_ltcg', 0):,}
- Realized STCG: ₹{tax_info.get('realized_stcg', 0):,}
- Dividend Income: ₹{tax_info.get('dividend_income', 0):,}
- Days until FY end: {tax_info.get('days_to_fy_end', 90)}

Portfolio Holdings: {len(portfolio)} positions

Provide:
1. Actions to take before March 31
2. Tax-saving opportunities still available
3. Charitable giving strategies (80G deductions)
4. ELSS investments for 80C
5. Advance tax payment optimization
6. Carry-forward loss opportunities
7. Next FY tax planning preview

Create a timeline of actions with deadlines.
"""
        
        planning = self.generate_response(prompt, temperature=0.4)
        
        return {
            "agent": self.agent_name,
            "analysis": planning,
            "type": "year_end_tax_planning"
        }
