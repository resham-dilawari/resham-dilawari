"""
Financial Health Analysis Agent
Analyzes financial statements, credit ratings, liquidity risks
"""
from typing import Dict, Any
from .underwriting_base import UnderwritingBaseAgent


class FinancialHealthAgent(UnderwritingBaseAgent):
    """
    Analyzes merchant's financial health to assess credit and default risks.
    Reviews financial statements, ratios, cash flow, debt levels.
    """
    
    def __init__(self):
        super().__init__(
            agent_name="Financial Health Analysis Agent",
            specialization="financial statement analysis, liquidity assessment, credit risk evaluation, solvency metrics"
        )
    
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze financial health of merchant.
        
        Expected data keys:
        - company_name: Business name
        - financial_data: Dict with revenue, profit, assets, liabilities, etc.
        - credit_rating: If available
        - years_in_business: Company age
        """
        self.log_action("financial_health_analysis_start", {"company": data.get("company_name")})
        
        company_name = data.get("company_name", "Unknown Company")
        financial_data = data.get("financial_data", {})
        credit_rating = data.get("credit_rating", "Not available")
        years_in_business = data.get("years_in_business", "Unknown")
        
        prompt = f"""Analyze the financial health of this merchant:

**Company**: {company_name}
**Years in Business**: {years_in_business}
**Credit Rating**: {credit_rating}

**Financial Data**:
{self._format_financial_data(financial_data)}

Your task:
1. Assess overall financial health
2. Calculate key financial ratios (if data available)
3. Identify liquidity risks
4. Flag any concerning financial patterns

**Key Metrics to Analyze:**

**Liquidity:**
- Current Ratio (Current Assets / Current Liabilities) - Healthy: > 1.5
- Quick Ratio (Cash + Receivables / Current Liabilities) - Healthy: > 1.0
- Cash on hand vs monthly burn rate

**Solvency:**
- Debt-to-Equity Ratio - Concern if > 2.0
- Interest Coverage Ratio (EBIT / Interest) - Healthy: > 3.0

**Profitability:**
- Net Profit Margin
- Revenue growth trend
- Operating cash flow positive?

**Warning Signs:**
- Negative equity
- Declining revenue for 2+ consecutive periods
- Cash burn exceeding cash reserves
- High debt with low profitability
- Recent losses after previous profits (sudden decline)
- Very new company (<1 year) with high credit requests

Output format:
## 💰 FINANCIAL HEALTH SUMMARY
[Overall assessment in 2-3 sentences]

## 📊 KEY FINANCIAL METRICS

### Liquidity:
- Current Ratio: [value] → [HEALTHY / CONCERN / CRITICAL]
- Quick Ratio: [value] → [HEALTHY / CONCERN / CRITICAL]
- Cash Position: [assessment]

### Solvency:
- Debt-to-Equity: [value] → [HEALTHY / CONCERN / CRITICAL]
- Total Debt: [amount]
- Equity: [amount]

### Profitability:
- Revenue: [amount and trend]
- Net Profit: [amount and margin]
- Operating Cash Flow: [POSITIVE / NEGATIVE]

## ⚠️ FINANCIAL RED FLAGS
[List any concerning indicators]

## 💡 CREDIT RISK ASSESSMENT
- Risk Level: [LOW / MEDIUM / HIGH / CRITICAL]
- Default Risk: [percentage or qualitative assessment]
- Recommended Credit Limit: [amount or NONE]

## 📋 UNDERWRITING RECOMMENDATION
[APPROVE / APPROVE WITH CONDITIONS / REQUEST MORE INFO / REJECT]

**Reasoning**: [Explain the recommendation]

IMPORTANT: If financial data is insufficient, state "Insufficient financial data for assessment" and recommend requesting financial statements.
"""
        
        analysis = self.generate_response(prompt, temperature=0.3)
        
        # Determine risk level
        risk_level = self._assess_financial_risk(analysis, financial_data)
        
        self.log_action("financial_health_analysis_complete", {
            "risk_level": risk_level,
            "has_financial_data": bool(financial_data)
        })
        
        return {
            "agent": self.agent_name,
            "analysis": analysis,
            "risk_level": risk_level,
            "financial_metrics": self._extract_key_metrics(financial_data),
            "timestamp": self.execution_log[-1]["timestamp"]
        }
    
    def _format_financial_data(self, financial_data: dict) -> str:
        """Format financial data for prompt."""
        if not financial_data:
            return "No financial data provided. Request financial statements from merchant."
        
        formatted = []
        
        # Revenue
        if "revenue" in financial_data:
            formatted.append(f"- Revenue: ₹{financial_data['revenue']:,}")
        
        # Profit/Loss
        if "net_profit" in financial_data:
            formatted.append(f"- Net Profit: ₹{financial_data['net_profit']:,}")
        
        # Assets
        if "total_assets" in financial_data:
            formatted.append(f"- Total Assets: ₹{financial_data['total_assets']:,}")
        
        # Liabilities
        if "total_liabilities" in financial_data:
            formatted.append(f"- Total Liabilities: ₹{financial_data['total_liabilities']:,}")
        
        # Cash
        if "cash" in financial_data:
            formatted.append(f"- Cash & Equivalents: ₹{financial_data['cash']:,}")
        
        # Debt
        if "total_debt" in financial_data:
            formatted.append(f"- Total Debt: ₹{financial_data['total_debt']:,}")
        
        if not formatted:
            return "Financial data provided but key metrics missing."
        
        return "\n".join(formatted)
    
    def _extract_key_metrics(self, financial_data: dict) -> dict:
        """Calculate key financial ratios if data available."""
        metrics = {}
        
        if "current_assets" in financial_data and "current_liabilities" in financial_data:
            if financial_data["current_liabilities"] > 0:
                metrics["current_ratio"] = financial_data["current_assets"] / financial_data["current_liabilities"]
        
        if "total_debt" in financial_data and "total_equity" in financial_data:
            if financial_data["total_equity"] > 0:
                metrics["debt_to_equity"] = financial_data["total_debt"] / financial_data["total_equity"]
        
        if "net_profit" in financial_data and "revenue" in financial_data:
            if financial_data["revenue"] > 0:
                metrics["profit_margin"] = (financial_data["net_profit"] / financial_data["revenue"]) * 100
        
        return metrics
    
    def _assess_financial_risk(self, analysis: str, financial_data: dict) -> str:
        """Determine financial risk level."""
        analysis_upper = analysis.upper()
        
        # Check analysis text
        if "CRITICAL" in analysis_upper or "REJECT" in analysis_upper:
            return "CRITICAL"
        elif "HIGH" in analysis_upper and "RISK" in analysis_upper:
            return "HIGH"
        elif "CONCERN" in analysis_upper:
            return "MEDIUM"
        elif "HEALTHY" in analysis_upper:
            return "LOW"
        
        # Check financial data directly
        if financial_data:
            if financial_data.get("net_profit", 0) < 0:
                return "HIGH"  # Losses
            if financial_data.get("cash", 0) < 0:
                return "CRITICAL"  # Negative cash
        
        return "MEDIUM"  # Default if unclear
