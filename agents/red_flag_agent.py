"""
Red Flag Detection Agent
Scans for negative news, lawsuits, fraud, bankruptcy, regulatory fines
"""
from typing import Dict, Any
from .underwriting_base import UnderwritingBaseAgent


class RedFlagAgent(UnderwritingBaseAgent):
    """
    Specialized agent for detecting red flags in merchant applications.
    Focuses on negative news, lawsuits, fraud indicators, regulatory issues.
    """
    
    def __init__(self):
        super().__init__(
            agent_name="Red Flag Detection Agent",
            specialization="negative news scanning, fraud detection, lawsuit identification, regulatory compliance issues"
        )
    
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze merchant data for red flags.
        
        Expected data keys:
        - company_name: Legal business name
        - directors: List of director names
        - registration_number: CIN/UEN
        - simulated_news: Simulated news data (in real system, would call News API)
        """
        self.log_action("red_flag_scan_start", {"company": data.get("company_name")})
        
        company_name = data.get("company_name", "Unknown Company")
        directors = data.get("directors", [])
        registration_number = data.get("registration_number", "N/A")
        
        # Simulate news search (in production, would use actual News API)
        simulated_news = data.get("simulated_news", [])
        
        prompt = f"""Analyze the following merchant for RED FLAGS:

**Company**: {company_name}
**Registration Number**: {registration_number}
**Directors**: {', '.join(directors) if directors else 'Not provided'}

**Recent News Data** (simulated):
{self._format_news_data(simulated_news)}

Your task:
1. Identify ALL red flags from the data
2. Categorize red flags by severity (CRITICAL, HIGH, MEDIUM, LOW)
3. For EACH red flag, provide:
   - Clear description
   - Source/evidence
   - Potential impact on underwriting decision
   
Red flag categories to check:
- Fraud allegations or convictions
- Bankruptcy filings or financial distress
- Lawsuits (pending or settled)
- Regulatory fines or sanctions
- Money laundering concerns
- Business license revocations
- Director-level issues (criminal records, previous company failures)
- Negative customer reviews (if severe pattern)

Output format:
## 🚨 RED FLAGS SUMMARY
[Total count and severity breakdown]

## CRITICAL RED FLAGS (Immediate Rejection)
- [Flag 1 with evidence and source]
- [Flag 2...]

## HIGH SEVERITY RED FLAGS (Requires Senior Review)
- [Flag 1 with evidence]

## MEDIUM SEVERITY RED FLAGS (Monitor Closely)
- [Flag 1 with evidence]

## LOW SEVERITY RED FLAGS (Note for File)
- [Flag 1...]

## ✅ NO RED FLAGS FOUND
[If none found, state clearly]

**Risk Recommendation**: [REJECT / ESCALATE / APPROVE WITH CONDITIONS / APPROVE]

IMPORTANT: If no negative information found, clearly state "No red flags detected" rather than guessing.
"""
        
        analysis = self.generate_response(prompt, temperature=0.2)  # Very low temp for accuracy
        
        # Determine risk level based on analysis
        risk_level = self._calculate_risk_level(analysis)
        
        self.log_action("red_flag_scan_complete", {
            "risk_level": risk_level,
            "red_flags_found": "YES" if any(word in analysis.upper() for word in ["CRITICAL", "HIGH SEVERITY"]) else "NO"
        })
        
        return {
            "agent": self.agent_name,
            "analysis": analysis,
            "risk_level": risk_level,
            "timestamp": self.execution_log[-1]["timestamp"]
        }
    
    def _format_news_data(self, news_data: list) -> str:
        """Format simulated news data for prompt."""
        if not news_data:
            return "No recent news data available."
        
        formatted = []
        for i, item in enumerate(news_data, 1):
            formatted.append(f"{i}. {item.get('headline', 'N/A')}")
            formatted.append(f"   Source: {item.get('source', 'N/A')}")
            formatted.append(f"   Date: {item.get('date', 'N/A')}")
            formatted.append(f"   Summary: {item.get('summary', 'N/A')}\n")
        
        return "\n".join(formatted)
    
    def _calculate_risk_level(self, analysis: str) -> str:
        """Determine overall risk level from analysis text."""
        analysis_upper = analysis.upper()
        
        if "CRITICAL RED FLAG" in analysis_upper or "IMMEDIATE REJECTION" in analysis_upper:
            return "CRITICAL"
        elif "HIGH SEVERITY" in analysis_upper or "REQUIRES SENIOR REVIEW" in analysis_upper:
            return "HIGH"
        elif "MEDIUM SEVERITY" in analysis_upper:
            return "MEDIUM"
        elif "LOW SEVERITY" in analysis_upper:
            return "LOW"
        elif "NO RED FLAGS" in analysis_upper:
            return "CLEAN"
        else:
            return "UNKNOWN"
