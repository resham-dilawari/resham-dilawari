"""
Input and Output Guardrails for AI Advisor Systems
PRD Requirements: Safety filters and validation
"""
import re
from typing import Tuple, Dict, Any
from google import genai
import os
import json


class InputGuardrails:
    """
    Input guardrails to filter and validate user queries.
    PRD Requirement: Block non-equity queries and definitive advice requests.
    """
    
    def __init__(self):
        # Initialize lightweight classifier
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key:
            self.client = genai.Client(api_key=api_key)
        else:
            self.client = None
    
    def validate_query(self, query: str, context: str = "stock_advisor") -> Tuple[bool, str]:
        """
        Validate if query is appropriate for the system.
        
        Returns:
            (is_valid, reason_if_invalid)
        """
        # Quick pattern-based checks first (fast)
        is_valid, reason = self._quick_validation(query, context)
        if not is_valid:
            return False, reason
        
        # LLM-based deep validation (slower but accurate)
        if self.client:
            return self._llm_validation(query, context)
        
        return True, ""
    
    def _quick_validation(self, query: str, context: str) -> Tuple[bool, str]:
        """Fast pattern-based validation."""
        query_lower = query.lower()
        
        # Check for empty/too short
        if len(query.strip()) < 5:
            return False, "Query too short. Please provide more details."
        
        # Check for too long
        if len(query) > 1000:
            return False, "Query too long. Please keep it under 1000 characters."
        
        # Context-specific validation
        if context == "stock_advisor":
            # Check for definitive advice requests
            definitive_patterns = [
                r'\bshould i (buy|sell|hold)\b',
                r'\btell me to (buy|sell)\b',
                r'\bmake.*decision for me\b',
                r'\bguarantee\b',
                r'\bsure.*profit\b',
                r'\bpromise.*return\b'
            ]
            
            for pattern in definitive_patterns:
                if re.search(pattern, query_lower):
                    return False, "⚠️ We provide analysis, not definitive buy/sell advice. Please rephrase as: 'What are the pros and cons of...' or 'What's the risk of...'"
            
            # Check for non-financial queries
            off_topic_patterns = [
                r'\bweather\b',
                r'\brecipe\b',
                r'\bmovie\b',
                r'\bsports?\b.*\b(score|game)\b',
                r'\bpolitics\b',
                r'\breligion\b'
            ]
            
            for pattern in off_topic_patterns:
                if re.search(pattern, query_lower):
                    return False, "❌ Please ask questions about stocks, equities, or financial markets only."
        
        elif context == "merchant_underwriting":
            # Underwriting-specific validation
            if "stock" in query_lower and "equity" in query_lower:
                return False, "❌ This is merchant underwriting. For stock analysis, use Stock Advisor."
        
        return True, ""
    
    def _llm_validation(self, query: str, context: str) -> Tuple[bool, str]:
        """LLM-based validation for complex cases."""
        
        if context == "stock_advisor":
            prompt = f"""You are a query validator for a stock analysis system.

User query: "{query}"

Validate if this query is:
1. Related to stocks, equities, or financial markets
2. NOT asking for definitive buy/sell advice
3. Appropriate for a stock research tool

Respond in JSON format:
{{
    "is_valid": true/false,
    "reason": "explanation if invalid"
}}

Examples:
- "Tell me about RELIANCE stock" → valid
- "What are risks of TCS?" → valid
- "Should I buy INFY now?" → INVALID (definitive advice)
- "What's the weather?" → INVALID (off-topic)
"""
        
        else:  # merchant_underwriting
            prompt = f"""You are a query validator for a merchant underwriting system.

User query: "{query}"

Validate if this query is related to business entity screening, KYC/KYB, or risk assessment.

Respond in JSON format:
{{
    "is_valid": true/false,
    "reason": "explanation if invalid"
}}
"""
        
        try:
            response = self.client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt,
                config={
                    'temperature': 0.1,
                    'max_output_tokens': 200,
                    'response_mime_type': 'application/json'
                }
            )
            
            # Parse JSON response
            response_text = response.text.strip()
            result = json.loads(response_text)
            
            if result.get("is_valid", True):
                return True, ""
            else:
                return False, result.get("reason", "Query not appropriate for this system.")
            
        except Exception as e:
            # If LLM fails, allow query (fail open)
            print(f"LLM validation error: {e}")
            return True, ""


class OutputGuardrails:
    """
    Output guardrails to validate AI-generated responses.
    PRD Requirement: Fact-checking, disclaimer enforcement, hallucination prevention.
    """
    
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key:
            self.client = genai.Client(api_key=api_key)
        else:
            self.client = None
    
    def validate_output(self, output: str, context: Dict[str, Any]) -> Tuple[bool, str, str]:
        """
        Validate AI-generated output before showing to user.
        
        Returns:
            (is_valid, sanitized_output, warning_message)
        """
        # Quick checks
        sanitized = output
        warnings = []
        
        # 1. Check for disclaimer
        has_disclaimer = self._check_disclaimer(output)
        if not has_disclaimer:
            # Add mandatory disclaimer
            sanitized = self._add_disclaimer(sanitized, context.get("product", "stock_advisor"))
            warnings.append("Added mandatory disclaimer")
        
        # 2. Check for PII (basic)
        sanitized, pii_found = self._redact_pii(sanitized)
        if pii_found:
            warnings.append("PII detected and redacted")
        
        # 3. Check for hallucinated numbers (if we have ground truth)
        if context.get("ground_truth_data"):
            is_valid, hallucination_warning = self._check_hallucinations(sanitized, context["ground_truth_data"])
            if not is_valid:
                warnings.append(hallucination_warning)
        
        # 4. Check for excessive confidence/promises
        sanitized, confidence_warning = self._check_excessive_confidence(sanitized)
        if confidence_warning:
            warnings.append(confidence_warning)
        
        warning_message = " | ".join(warnings) if warnings else ""
        
        return True, sanitized, warning_message
    
    def _check_disclaimer(self, text: str) -> bool:
        """Check if mandatory disclaimer is present."""
        disclaimer_phrases = [
            "not financial advice",
            "not investment advice",
            "consult.*financial advisor",
            "past performance.*not.*guarantee"
        ]
        
        text_lower = text.lower()
        return any(re.search(phrase, text_lower) for phrase in disclaimer_phrases)
    
    def _add_disclaimer(self, text: str, product: str) -> str:
        """Add mandatory disclaimer to output."""
        if product == "stock_advisor":
            disclaimer = "\n\n---\n\n**⚠️ Disclaimer**: This analysis is for informational purposes only and does not constitute financial advice. Consult with a qualified financial advisor before making investment decisions. Past performance is not indicative of future results."
        else:  # merchant_underwriting
            disclaimer = "\n\n---\n\n**⚠️ Disclaimer**: This risk assessment is generated by an AI system. Final approval authority rests with human underwriters and senior management. All findings must be verified through additional due diligence."
        
        return text + disclaimer
    
    def _redact_pii(self, text: str) -> Tuple[str, bool]:
        """Basic PII redaction (email, phone, SSN patterns)."""
        pii_found = False
        sanitized = text
        
        # Email patterns
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.search(email_pattern, sanitized):
            sanitized = re.sub(email_pattern, '[EMAIL REDACTED]', sanitized)
            pii_found = True
        
        # Phone patterns (simple)
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        if re.search(phone_pattern, sanitized):
            sanitized = re.sub(phone_pattern, '[PHONE REDACTED]', sanitized)
            pii_found = True
        
        # SSN/Aadhaar patterns
        ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
        if re.search(ssn_pattern, sanitized):
            sanitized = re.sub(ssn_pattern, '[ID REDACTED]', sanitized)
            pii_found = True
        
        aadhaar_pattern = r'\b\d{4}\s?\d{4}\s?\d{4}\b'
        if re.search(aadhaar_pattern, sanitized):
            sanitized = re.sub(aadhaar_pattern, '[AADHAAR REDACTED]', sanitized)
            pii_found = True
        
        return sanitized, pii_found
    
    def _check_hallucinations(self, text: str, ground_truth: Dict[str, Any]) -> Tuple[bool, str]:
        """Check for hallucinated financial numbers."""
        # Extract numbers from text
        number_pattern = r'\b\d+\.?\d*\b'
        text_numbers = re.findall(number_pattern, text)
        
        # If we have P/E ratio in ground truth, check if AI made it up
        if "pe_ratio" in ground_truth:
            true_pe = float(ground_truth["pe_ratio"])
            
            # Check if text mentions P/E ratio with wrong number
            pe_mentions = re.finditer(r'P/E.*?(\d+\.?\d*)', text, re.IGNORECASE)
            for match in pe_mentions:
                mentioned_pe = float(match.group(1))
                # Allow 10% tolerance for rounding
                if abs(mentioned_pe - true_pe) / true_pe > 0.1:
                    return False, f"⚠️ Hallucinated P/E ratio detected: {mentioned_pe} (actual: {true_pe})"
        
        return True, ""
    
    def _check_excessive_confidence(self, text: str) -> Tuple[str, str]:
        """Flag and soften excessive confidence/promises."""
        warning = ""
        sanitized = text
        
        # Problematic phrases
        excessive_phrases = {
            r'\bguaranteed?\b': 'likely',
            r'\bcertainly will\b': 'may',
            r'\bdefinitely\b': 'probably',
            r'\b100% sure\b': 'confident',
            r'\bwill definitely\b': 'is expected to',
            r'\bcannot fail\b': 'has strong potential'
        }
        
        for pattern, replacement in excessive_phrases.items():
            if re.search(pattern, sanitized, re.IGNORECASE):
                sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)
                warning = "Softened excessive confidence language"
        
        return sanitized, warning


# Convenience functions
def validate_input(query: str, context: str = "stock_advisor") -> Tuple[bool, str]:
    """Quick access to input validation."""
    guardrails = InputGuardrails()
    return guardrails.validate_query(query, context)


def validate_output(output: str, context: Dict[str, Any] = None) -> Tuple[bool, str, str]:
    """Quick access to output validation."""
    if context is None:
        context = {"product": "stock_advisor"}
    guardrails = OutputGuardrails()
    return guardrails.validate_output(output, context)
