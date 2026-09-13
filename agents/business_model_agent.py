"""
Business Model Analysis Agent
Determines what the business actually does and checks against Acceptable Use Policy
"""
from typing import Dict, Any
from .underwriting_base import UnderwritingBaseAgent


class BusinessModelAgent(UnderwritingBaseAgent):
    """
    Analyzes merchant's business model to ensure compliance with Acceptable Use Policy.
    Identifies prohibited businesses (gambling, adult content, weapons, etc.)
    """
    
    def __init__(self):
        super().__init__(
            agent_name="Business Model Analysis Agent",
            specialization="business model identification, acceptable use policy compliance, prohibited business detection"
        )
    
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze business model and check against AUP.
        
        Expected data keys:
        - company_name: Business name
        - business_description: What the company does
        - website: Company website
        - industry: Industry classification
        """
        self.log_action("business_model_analysis_start", {"company": data.get("company_name")})
        
        company_name = data.get("company_name", "Unknown Company")
        business_description = data.get("business_description", "Not provided")
        website = data.get("website", "N/A")
        industry = data.get("industry", "N/A")
        
        prompt = f"""Analyze this merchant's business model for Acceptable Use Policy compliance:

**Company**: {company_name}
**Website**: {website}
**Industry**: {industry}
**Business Description**: {business_description}

Your task:
1. Provide a clear 2-3 sentence summary of what this business actually does
2. Identify the core business model (B2B/B2C, product/service, revenue model)
3. Check against PROHIBITED BUSINESS CATEGORIES:

**HIGH RISK / PROHIBITED:**
- Adult content or services
- Gambling, betting, online casinos
- Weapons, ammunition, explosives
- Illegal drugs or drug paraphernalia
- Money laundering services
- Ponzi schemes or pyramid schemes
- Counterfeit goods
- Hacking tools or services
- Tobacco products (in some jurisdictions)
- Cryptocurrency exchanges (high AML risk)

**MEDIUM RISK (Requires Extra Scrutiny):**
- Forex trading platforms
- Multi-level marketing (MLM)
- Nutraceuticals / unregulated supplements
- High-value luxury goods
- Travel agencies (chargeback risk)
- Digital content downloads

**LOW RISK (Generally Acceptable):**
- E-commerce (legitimate goods)
- SaaS / Software services
- Professional services
- Education / EdTech
- Healthcare services
- Manufacturing / Distribution

Output format:
## 📋 BUSINESS MODEL SUMMARY
[Clear 2-3 sentence description of what they do]

## 🏢 BUSINESS TYPE
- Model: [B2B/B2C/Marketplace]
- Category: [Industry category]
- Revenue: [How they make money]

## ⚠️ ACCEPTABLE USE POLICY CHECK

### Prohibited Business Check:
[List any matches with prohibited categories]

### Risk Level: [PROHIBITED / HIGH RISK / MEDIUM RISK / LOW RISK]

### Compliance Status: [REJECT / FLAG FOR REVIEW / APPROVE]

### Reasoning:
[Explain why this is the recommended action]

## 💡 ADDITIONAL NOTES
[Any other relevant observations about the business model]

IMPORTANT: If unclear, say "Insufficient data to determine business model" rather than guessing.
"""
        
        analysis = self.generate_response(prompt, temperature=0.3)
        
        # Determine compliance status
        compliance_status = self._determine_compliance(analysis)
        
        self.log_action("business_model_analysis_complete", {
            "compliance_status": compliance_status,
            "business_type": industry
        })
        
        return {
            "agent": self.agent_name,
            "analysis": analysis,
            "compliance_status": compliance_status,
            "risk_level": self._map_compliance_to_risk(compliance_status),
            "timestamp": self.execution_log[-1]["timestamp"]
        }
    
    def _determine_compliance(self, analysis: str) -> str:
        """Extract compliance status from analysis."""
        analysis_upper = analysis.upper()
        
        if "PROHIBITED" in analysis_upper or "REJECT" in analysis_upper:
            return "PROHIBITED"
        elif "HIGH RISK" in analysis_upper or "FLAG FOR REVIEW" in analysis_upper:
            return "HIGH_RISK"
        elif "MEDIUM RISK" in analysis_upper:
            return "MEDIUM_RISK"
        elif "LOW RISK" in analysis_upper or "APPROVE" in analysis_upper:
            return "LOW_RISK"
        else:
            return "UNKNOWN"
    
    def _map_compliance_to_risk(self, compliance_status: str) -> str:
        """Map compliance status to risk level."""
        mapping = {
            "PROHIBITED": "CRITICAL",
            "HIGH_RISK": "HIGH",
            "MEDIUM_RISK": "MEDIUM",
            "LOW_RISK": "LOW",
            "UNKNOWN": "MEDIUM"
        }
        return mapping.get(compliance_status, "MEDIUM")
