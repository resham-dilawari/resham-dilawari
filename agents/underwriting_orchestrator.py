"""
Underwriting Orchestrator Agent
Coordinates all underwriting agents and synthesizes risk assessment brief
"""
from typing import Dict, Any, List
from .underwriting_base import UnderwritingBaseAgent
from .red_flag_agent import RedFlagAgent
from .business_model_agent import BusinessModelAgent
from .financial_health_agent import FinancialHealthAgent
from .sanctions_watchlist_agent import SanctionsWatchlistAgent
from concurrent.futures import ThreadPoolExecutor


class UnderwritingOrchestrator(UnderwritingBaseAgent):
    """
    Master orchestrator for merchant underwriting.
    Coordinates specialized agents and produces final risk assessment brief.
    """
    
    def __init__(self):
        super().__init__(
            agent_name="Underwriting Orchestrator",
            specialization="merchant underwriting coordination, risk synthesis, final decision-making"
        )
        
        # Initialize all specialized agents
        self.agents = {
            "red_flag": RedFlagAgent(),
            "business_model": BusinessModelAgent(),
            "financial_health": FinancialHealthAgent(),
            "sanctions": SanctionsWatchlistAgent()
        }
    
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main underwriting workflow.
        
        Expected data:
        - company_name: Legal business name
        - registration_number: CIN/UEN
        - directors: List of director names
        - business_description: What company does
        - financial_data: Financial statements
        - website: Company website
        - Additional fields as needed
        """
        self.log_action("underwriting_start", {
            "company": data.get("company_name"),
            "registration": data.get("registration_number")
        })
        
        agent_results = {}
        
        # Execute agents in parallel
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                "red_flag": executor.submit(self.agents["red_flag"].analyze, data),
                "business_model": executor.submit(self.agents["business_model"].analyze, data),
                "financial_health": executor.submit(self.agents["financial_health"].analyze, data),
                "sanctions": executor.submit(self.agents["sanctions"].analyze, data),
            }
            
            for agent_name, future in futures.items():
                try:
                    agent_results[agent_name] = future.result(timeout=30)
                except Exception as e:
                    agent_results[agent_name] = {"error": str(e), "risk_level": "UNKNOWN"}
        
        # Synthesize final risk assessment
        synthesis = self._synthesize_risk_brief(agent_results, data)
        
        # Calculate overall risk score
        overall_risk = self._calculate_overall_risk(agent_results)
        
        # Make final decision
        decision = self._make_final_decision(overall_risk, agent_results)
        
        self.log_action("underwriting_complete", {
            "overall_risk": overall_risk,
            "decision": decision
        })
        
        return {
            "orchestrator": self.agent_name,
            "agent_results": agent_results,
            "synthesis": synthesis,
            "overall_risk": overall_risk,
            "decision": decision,
            "timestamp": self.execution_log[-1]["timestamp"]
        }
    
    def _synthesize_risk_brief(self, agent_results: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Synthesize all agent findings into executive risk brief."""
        
        company_name = context.get("company_name", "Unknown")
        registration = context.get("registration_number", "N/A")
        
        # Prepare agent summaries
        agent_summaries = "\n\n".join([
            f"**{agent_name.upper().replace('_', ' ')} AGENT:**\n{result.get('analysis', result)}"
            for agent_name, result in agent_results.items()
            if not result.get("error")
        ])
        
        prompt = f"""{self.get_system_prompt()}

You are synthesizing a merchant underwriting risk assessment for:
**Company**: {company_name}
**Registration**: {registration}

AGENT FINDINGS:
{agent_summaries}

Your task:
Create an executive risk assessment brief for the risk analyst. This must be:
1. Concise but comprehensive
2. Highlight ALL critical red flags prominently
3. Provide clear, actionable recommendation
4. Include confidence level
5. List required follow-up actions

Output format:

# 🏢 MERCHANT RISK ASSESSMENT BRIEF

**Merchant**: {company_name}
**Registration**: {registration}
**Assessment Date**: [Today's date]
**Analyst**: AI Underwriting System

---

## 🎯 EXECUTIVE SUMMARY
[2-3 sentence overview of merchant and key findings]

---

## 🚨 CRITICAL FINDINGS
[List ANY critical red flags that require immediate attention]
[If none, state "No critical findings"]

---

## ⚠️ KEY RISK FACTORS

### Red Flags:
[Summary from Red Flag Agent]

### Business Model Compliance:
[Summary from Business Model Agent]

### Financial Health:
[Summary from Financial Health Agent]

### Sanctions/AML:
[Summary from Sanctions Agent]

---

## 📊 RISK SCORING

| Category | Risk Level | Weight | Notes |
|----------|-----------|--------|-------|
| Red Flags | [LEVEL] | 30% | [Brief note] |
| Business Model | [LEVEL] | 25% | [Brief note] |
| Financial Health | [LEVEL] | 25% | [Brief note] |
| Sanctions/AML | [LEVEL] | 20% | [Brief note] |

**Overall Risk Score**: [LOW / MEDIUM / HIGH / CRITICAL]

---

## ✅ RECOMMENDATION

**Decision**: [APPROVE / APPROVE WITH CONDITIONS / REQUEST MORE INFO / REJECT]

**Confidence Level**: [percentage]

**Reasoning**:
[Clear explanation of why this decision was reached]

**Conditions** (if APPROVE WITH CONDITIONS):
- [Condition 1]
- [Condition 2]

**Additional Information Required** (if REQUEST MORE INFO):
- [Info needed 1]
- [Info needed 2]

---

## 📋 REQUIRED ACTIONS

**Immediate**:
- [Action 1]

**Before Approval**:
- [Action 2]

**Ongoing Monitoring**:
- [Action 3]

---

## 📎 SOURCE CITATIONS
[All sources used in this assessment]

---

**Audit Trail**: All agent execution logs available for compliance review.
**Next Steps**: [What the analyst should do next]

---

*This assessment was generated by an AI system. Final approval authority rests with human underwriters and senior management.*
"""
        
        synthesis = self.generate_response(prompt, temperature=0.4)
        
        self.log_action("synthesis_complete", {"success": True})
        
        return synthesis
    
    def _calculate_overall_risk(self, agent_results: Dict[str, Any]) -> str:
        """Calculate overall risk level from agent results."""
        
        risk_levels = []
        for agent_name, result in agent_results.items():
            if "risk_level" in result:
                risk_levels.append(result["risk_level"])
        
        # Map risk to numeric scores
        risk_scores = {
            "CRITICAL": 4,
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1,
            "CLEAN": 0,
            "UNKNOWN": 2  # Default to medium if unknown
        }
        
        # Calculate weighted average (any CRITICAL = overall CRITICAL)
        if "CRITICAL" in risk_levels:
            return "CRITICAL"
        elif risk_levels.count("HIGH") >= 2:
            return "HIGH"
        elif "HIGH" in risk_levels:
            return "HIGH"
        elif risk_levels.count("MEDIUM") >= 2:
            return "MEDIUM"
        elif "MEDIUM" in risk_levels:
            return "MEDIUM"
        elif all(r in ["LOW", "CLEAN"] for r in risk_levels):
            return "LOW"
        else:
            return "MEDIUM"
    
    def _make_final_decision(self, overall_risk: str, agent_results: Dict[str, Any]) -> str:
        """Make final underwriting decision based on risk level."""
        
        # Auto-reject logic
        if overall_risk == "CRITICAL":
            return "REJECT"
        
        # Check for prohibited business
        business_result = agent_results.get("business_model", {})
        if business_result.get("compliance_status") == "PROHIBITED":
            return "REJECT"
        
        # Check for sanctions matches
        sanctions_result = agent_results.get("sanctions", {})
        if sanctions_result.get("risk_level") == "CRITICAL":
            return "REJECT"
        
        # Conditional approval logic
        if overall_risk == "HIGH":
            return "REQUEST_MORE_INFO"
        
        if overall_risk == "MEDIUM":
            return "APPROVE_WITH_CONDITIONS"
        
        if overall_risk == "LOW":
            return "APPROVE"
        
        return "REQUEST_MORE_INFO"  # Default
    
    def get_agent_health_status(self) -> Dict[str, Any]:
        """Check health status of all underwriting agents."""
        status = {}
        for name, agent in self.agents.items():
            status[name] = {
                "name": agent.agent_name,
                "specialization": agent.specialization,
                "execution_log_size": len(agent.get_execution_log()),
                "status": "healthy"
            }
        return status
