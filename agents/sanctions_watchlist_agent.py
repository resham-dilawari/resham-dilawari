"""
Sanctions & Watchlist Screening Agent
Checks company and directors against regulatory watchlists (RBI, MAS, OFAC, UN, etc.)
"""
from typing import Dict, Any, List
from .underwriting_base import UnderwritingBaseAgent


class SanctionsWatchlistAgent(UnderwritingBaseAgent):
    """
    Screens merchants and directors against sanctions lists and regulatory watchlists.
    Critical for AML (Anti-Money Laundering) compliance.
    """
    
    def __init__(self):
        super().__init__(
            agent_name="Sanctions & Watchlist Screening Agent",
            specialization="sanctions list screening, AML watchlist checking, PEP (Politically Exposed Persons) identification, regulatory compliance"
        )
    
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Screen against sanctions and watchlists.
        
        Expected data keys:
        - company_name: Business legal name
        - directors: List of director names
        - registration_number: CIN/UEN
        - country: Country of operations
        - simulated_watchlist_check: Simulated results (in prod, would call actual APIs)
        """
        self.log_action("sanctions_screening_start", {"company": data.get("company_name")})
        
        company_name = data.get("company_name", "Unknown Company")
        directors = data.get("directors", [])
        registration_number = data.get("registration_number", "N/A")
        country = data.get("country", "India")
        
        # Simulate watchlist check (in production, would call actual APIs)
        watchlist_results = data.get("simulated_watchlist_check", self._simulate_watchlist_check(company_name, directors))
        
        prompt = f"""Perform sanctions and watchlist screening for this merchant:

**Company**: {company_name}
**Registration**: {registration_number}
**Country**: {country}
**Directors**: {', '.join(directors) if directors else 'Not provided'}

**WATCHLISTS TO CHECK:**

**Critical Lists (Auto-Reject if Match):**
1. OFAC (Office of Foreign Assets Control) - US Sanctions
2. UN Sanctions List
3. EU Sanctions List
4. RBI (Reserve Bank of India) - Defaulters/Fraudulent entities
5. MAS (Monetary Authority of Singapore) - If Singapore entity
6. Interpol Red Notices
7. Financial Action Task Force (FATF) Grey/Black Lists

**Important Lists (Requires Investigation):**
8. PEP Lists (Politically Exposed Persons)
9. Adverse Media Lists
10. Corporate Registry Debarred Lists
11. Previous Fraud Convictions Lists

**Screening Results** (simulated):
{self._format_watchlist_results(watchlist_results)}

Your task:
1. Evaluate each match (TRUE MATCH vs FALSE POSITIVE)
2. Assess severity of any confirmed matches
3. Determine AML/CFT (Anti-Money Laundering / Counter-Financing of Terrorism) risk
4. Provide clear recommendation

Output format:
## 🔍 WATCHLIST SCREENING RESULTS

### Company Screening:
- OFAC: [CLEAR / MATCH / POTENTIAL MATCH]
- UN Sanctions: [CLEAR / MATCH / POTENTIAL MATCH]
- EU Sanctions: [CLEAR / MATCH / POTENTIAL MATCH]
- RBI Watchlist: [CLEAR / MATCH / POTENTIAL MATCH]
- Other Lists: [Results]

### Director Screening:
{self._format_director_screening(directors)}

## ⚠️ CONFIRMED MATCHES
[List any confirmed matches with details and severity]

## 🚨 CRITICAL FINDINGS
[Any findings that require immediate rejection]

## 💡 AML/CFT RISK ASSESSMENT
- Risk Level: [LOW / MEDIUM / HIGH / CRITICAL]
- PEP Exposure: [YES / NO]
- Sanctions Risk: [YES / NO]
- Geographic Risk: [LOW / MEDIUM / HIGH]

## 📋 UNDERWRITING RECOMMENDATION
[APPROVE / ENHANCED DUE DILIGENCE REQUIRED / ESCALATE TO COMPLIANCE / REJECT]

**Reasoning**: [Clear explanation of recommendation]

**Required Actions**: [Any follow-up actions needed]

IMPORTANT: 
- False positives are common (similar names). Verify with registration numbers, dates of birth, addresses.
- Any true match on critical sanctions lists = automatic rejection.
- Document reasoning for all match assessments (for audit trail).
"""
        
        analysis = self.generate_response(prompt, temperature=0.2)  # Very low temp for accuracy
        
        # Determine risk level
        risk_level = self._determine_sanctions_risk(analysis, watchlist_results)
        
        self.log_action("sanctions_screening_complete", {
            "risk_level": risk_level,
            "matches_found": watchlist_results.get("has_matches", False)
        })
        
        return {
            "agent": self.agent_name,
            "analysis": analysis,
            "risk_level": risk_level,
            "watchlist_results": watchlist_results,
            "timestamp": self.execution_log[-1]["timestamp"]
        }
    
    def _simulate_watchlist_check(self, company_name: str, directors: List[str]) -> dict:
        """
        Simulate watchlist screening results.
        In production, this would call actual watchlist APIs.
        """
        # For demo purposes, return clean results
        return {
            "company_matches": [],
            "director_matches": [],
            "has_matches": False,
            "lists_checked": ["OFAC", "UN Sanctions", "EU Sanctions", "RBI", "Interpol"],
            "screening_date": "2024-01-15"
        }
    
    def _format_watchlist_results(self, results: dict) -> str:
        """Format watchlist results for prompt."""
        if not results or not results.get("has_matches"):
            return "✅ NO MATCHES found across all checked watchlists."
        
        formatted = []
        
        if results.get("company_matches"):
            formatted.append("**Company Matches:**")
            for match in results["company_matches"]:
                formatted.append(f"- List: {match.get('list', 'N/A')}")
                formatted.append(f"  Name: {match.get('name', 'N/A')}")
                formatted.append(f"  Similarity: {match.get('similarity', 'N/A')}")
                formatted.append(f"  Details: {match.get('details', 'N/A')}\n")
        
        if results.get("director_matches"):
            formatted.append("**Director Matches:**")
            for match in results["director_matches"]:
                formatted.append(f"- Director: {match.get('director', 'N/A')}")
                formatted.append(f"  List: {match.get('list', 'N/A')}")
                formatted.append(f"  Similarity: {match.get('similarity', 'N/A')}")
                formatted.append(f"  Details: {match.get('details', 'N/A')}\n")
        
        return "\n".join(formatted) if formatted else "✅ NO MATCHES"
    
    def _format_director_screening(self, directors: List[str]) -> str:
        """Format director screening results."""
        if not directors:
            return "No directors provided for screening."
        
        formatted = []
        for director in directors:
            formatted.append(f"- {director}: [CLEAR / MATCH / POTENTIAL MATCH]")
        
        return "\n".join(formatted)
    
    def _determine_sanctions_risk(self, analysis: str, watchlist_results: dict) -> str:
        """Determine sanctions/AML risk level."""
        analysis_upper = analysis.upper()
        
        # Check for confirmed matches
        if watchlist_results.get("has_matches"):
            if any("OFAC" in str(m) or "UN" in str(m) for m in watchlist_results.get("company_matches", [])):
                return "CRITICAL"  # Critical list match
        
        # Check analysis text
        if "REJECT" in analysis_upper or "CRITICAL" in analysis_upper:
            return "CRITICAL"
        elif "ENHANCED DUE DILIGENCE" in analysis_upper or "HIGH" in analysis_upper:
            return "HIGH"
        elif "MEDIUM" in analysis_upper:
            return "MEDIUM"
        elif "CLEAR" in analysis_upper or "LOW" in analysis_upper:
            return "LOW"
        
        return "LOW"  # Default if no matches and no concerns
