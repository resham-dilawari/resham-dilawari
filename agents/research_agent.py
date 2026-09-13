"""
Market Research Agent
Specializes in sector analysis, macro trends, and market opportunity identification
"""
from typing import Dict, Any, List
from .base_agent import BaseAgent


class MarketResearchAgent(BaseAgent):
    """Agent specialized in market research, sector analysis, and macro trends."""
    
    def __init__(self):
        super().__init__(
            agent_name="Market Research Agent",
            specialization="sector trends, macroeconomic analysis, thematic investing, and opportunity identification"
        )
        
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Conduct market research and identify opportunities.
        
        Expected context:
        - sector: Specific sector to analyze (optional)
        - market_context: Current market conditions
        - user_preferences: Investment themes of interest
        """
        self.log_action("start_research", {"sector": context.get("sector", "broad market")})
        
        prompt = f"""{self.get_system_prompt()}

Conduct comprehensive market research for Indian markets:

Focus Area: {context.get('sector', 'Broad market analysis')}
Current Market Context: {context.get('market_context', 'Normal market conditions')}
User Interest Areas: {context.get('user_preferences', 'Growth and value opportunities')}

Provide detailed research including:
1. Sector/Theme Overview and growth drivers
2. Macroeconomic factors impacting the sector
3. Key trends and tailwinds
4. Regulatory environment and policy impact
5. Competitive landscape
6. Top companies in the sector with brief rationale
7. Risks and headwinds
8. Investment thesis and time horizon
9. Entry points and valuation considerations

Rate the sector opportunity: STRONG OPPORTUNITY / OPPORTUNITY / NEUTRAL / CAUTION / AVOID
Provide confidence level and key assumptions.
"""
        
        analysis_text = self.generate_response(prompt, temperature=0.6)
        
        result = {
            "agent": self.agent_name,
            "sector": context.get("sector", "broad market"),
            "analysis": analysis_text,
            "timestamp": self.execution_log[-1]["timestamp"] if self.execution_log else None,
            "type": "market_research"
        }
        
        self.log_action("complete_research", {"sector": context.get("sector")})
        
        return result
    
    def thematic_opportunities(self, themes: List[str]) -> Dict[str, Any]:
        """Identify investment opportunities in specific themes."""
        self.log_action("thematic_analysis", {"themes": themes})
        
        themes_list = ", ".join(themes)
        
        prompt = f"""{self.get_system_prompt()}

Analyze the following investment themes for Indian markets:
{themes_list}

For each theme:
1. Theme definition and growth potential
2. Market size and trajectory
3. Key players and beneficiaries in India
4. Time horizon for theme to play out
5. Risks to the theme
6. Specific stock recommendations
7. Expected returns profile

Rank themes by attractiveness and provide a balanced view.
"""
        
        thematic_analysis = self.generate_response(prompt, temperature=0.6)
        
        return {
            "agent": self.agent_name,
            "analysis": thematic_analysis,
            "type": "thematic_opportunities",
            "themes": themes
        }
    
    def macro_outlook(self, timeframe: str = "12 months") -> Dict[str, Any]:
        """Provide macroeconomic outlook and market implications."""
        self.log_action("macro_analysis", {"timeframe": timeframe})
        
        prompt = f"""{self.get_system_prompt()}

Provide macroeconomic outlook for Indian markets for the next {timeframe}:

Analyze:
1. GDP growth trajectory and drivers
2. Inflation outlook and RBI monetary policy
3. Currency (INR) outlook and implications
4. Global factors impacting India (Fed policy, crude oil, etc.)
5. Corporate earnings outlook
6. Valuation levels (expensive/fair/cheap)
7. Sector rotation recommendations
8. Key risks and opportunities
9. Asset allocation guidance (equity/debt/gold/cash)

Provide actionable investment strategy based on macro view.
Include confidence level and key trigger points to revisit the thesis.
"""
        
        macro_analysis = self.generate_response(prompt, temperature=0.6)
        
        return {
            "agent": self.agent_name,
            "analysis": macro_analysis,
            "type": "macro_outlook",
            "timeframe": timeframe
        }
    
    def emerging_opportunities(self, budget: float, risk_tolerance: str) -> Dict[str, Any]:
        """Identify emerging investment opportunities."""
        prompt = f"""{self.get_system_prompt()}

Identify emerging investment opportunities in Indian markets:

Investment Budget: ₹{budget:,.0f}
Risk Tolerance: {risk_tolerance}

Focus on:
1. Emerging sectors with high growth potential
2. Small/mid-cap hidden gems
3. Undervalued quality companies
4. New IPOs worth considering
5. Turnaround stories
6. Disruptive business models

For each opportunity:
- Why it's emerging now
- Risk/reward profile
- Entry strategy
- Exit criteria

Provide 5-7 specific actionable ideas.
"""
        
        opportunities = self.generate_response(prompt, temperature=0.7)
        
        return {
            "agent": self.agent_name,
            "analysis": opportunities,
            "type": "emerging_opportunities",
            "budget": budget
        }
