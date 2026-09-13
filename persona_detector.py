"""
Persona Detection and Adaptation System
Automatically detects user persona and adapts recommendations
"""
from typing import Dict, Any, Optional
import json


class PersonaDetector:
    """
    Detects user persona based on:
    1. Risk questionnaire responses
    2. Portfolio size
    3. Investment experience
    4. Goals and preferences
    """
    
    PERSONAS = {
        "novice_nisha": {
            "name": "Novice Nisha",
            "description": "Beginner investor, needs education and hand-holding",
            "characteristics": {
                "experience_years": (0, 2),
                "portfolio_size": (0, 500000),  # ₹0-5L
                "risk_tolerance": ["Very Conservative", "Conservative"],
                "goals": ["Learning", "Wealth Creation", "Savings"],
                "needs_education": True,
                "comfort_with_volatility": "Low",
                "investment_knowledge": "Basic"
            },
            "response_style": {
                "complexity": "simple",
                "jargon": "minimal",
                "explanations": "detailed",
                "examples": "many",
                "tone": "educational"
            }
        },
        "mid_career_mohit": {
            "name": "Mid-Career Mohit",
            "description": "Intermediate investor, wants efficiency and optimization",
            "characteristics": {
                "experience_years": (3, 10),
                "portfolio_size": (500000, 3000000),  # ₹5L-30L
                "risk_tolerance": ["Moderate", "Moderate-Aggressive"],
                "goals": ["Retirement", "Tax Saving", "Wealth Creation", "Children Education"],
                "needs_education": False,
                "comfort_with_volatility": "Medium",
                "investment_knowledge": "Intermediate"
            },
            "response_style": {
                "complexity": "moderate",
                "jargon": "acceptable",
                "explanations": "concise",
                "examples": "few",
                "tone": "professional"
            }
        },
        "sophisticated_sanjay": {
            "name": "Sophisticated Sanjay",
            "description": "Expert investor, wants advanced analytics",
            "characteristics": {
                "experience_years": (10, 50),
                "portfolio_size": (3000000, float('inf')),  # ₹30L+
                "risk_tolerance": ["Aggressive", "Very Aggressive"],
                "goals": ["Alpha Generation", "Wealth Preservation", "Alternative Investments"],
                "needs_education": False,
                "comfort_with_volatility": "High",
                "investment_knowledge": "Advanced"
            },
            "response_style": {
                "complexity": "advanced",
                "jargon": "technical",
                "explanations": "minimal",
                "examples": "rare",
                "tone": "institutional"
            }
        }
    }
    
    RISK_QUESTIONNAIRE = [
        {
            "id": "experience",
            "question": "How many years of investment experience do you have?",
            "type": "single_choice",
            "options": [
                {"value": 0, "label": "Less than 1 year", "score": {"novice": 3}},
                {"value": 1.5, "label": "1-2 years", "score": {"novice": 2}},
                {"value": 5, "label": "3-7 years", "score": {"mid_career": 3}},
                {"value": 10, "label": "8-10 years", "score": {"mid_career": 2}},
                {"value": 15, "label": "More than 10 years", "score": {"sophisticated": 3}}
            ]
        },
        {
            "id": "portfolio_size",
            "question": "What is your approximate investable portfolio size?",
            "type": "single_choice",
            "options": [
                {"value": 100000, "label": "Less than ₹2 lakhs", "score": {"novice": 3}},
                {"value": 350000, "label": "₹2-5 lakhs", "score": {"novice": 2}},
                {"value": 1000000, "label": "₹5-15 lakhs", "score": {"mid_career": 3}},
                {"value": 2500000, "label": "₹15-30 lakhs", "score": {"mid_career": 2}},
                {"value": 5000000, "label": "₹30 lakhs - ₹1 crore", "score": {"sophisticated": 2}},
                {"value": 15000000, "label": "More than ₹1 crore", "score": {"sophisticated": 3}}
            ]
        },
        {
            "id": "investment_knowledge",
            "question": "How would you rate your investment knowledge?",
            "type": "single_choice",
            "options": [
                {"value": 1, "label": "Beginner - I'm just starting to learn", "score": {"novice": 3}},
                {"value": 2, "label": "Basic - I understand stocks and mutual funds", "score": {"novice": 1, "mid_career": 1}},
                {"value": 3, "label": "Intermediate - I understand financial ratios and analysis", "score": {"mid_career": 3}},
                {"value": 4, "label": "Advanced - I understand options, derivatives, portfolio theory", "score": {"sophisticated": 2}},
                {"value": 5, "label": "Expert - I have professional finance background", "score": {"sophisticated": 3}}
            ]
        },
        {
            "id": "volatility_comfort",
            "question": "If your ₹1 lakh investment dropped to ₹70,000 in a month, you would:",
            "type": "single_choice",
            "options": [
                {"value": 1, "label": "Panic and sell everything immediately", "score": {"novice": 3}},
                {"value": 2, "label": "Feel very uncomfortable, consider selling", "score": {"novice": 2}},
                {"value": 3, "label": "Feel concerned but hold on", "score": {"mid_career": 3}},
                {"value": 4, "label": "See it as normal market volatility", "score": {"sophisticated": 2}},
                {"value": 5, "label": "See it as a buying opportunity", "score": {"sophisticated": 3}}
            ]
        },
        {
            "id": "investment_goal",
            "question": "What is your primary investment goal?",
            "type": "single_choice",
            "options": [
                {"value": "learning", "label": "Learning about investing", "score": {"novice": 3}},
                {"value": "savings", "label": "Safe savings with some returns", "score": {"novice": 2}},
                {"value": "wealth", "label": "Long-term wealth creation", "score": {"mid_career": 3}},
                {"value": "retirement", "label": "Retirement planning", "score": {"mid_career": 2}},
                {"value": "alpha", "label": "Beat the market (generate alpha)", "score": {"sophisticated": 3}},
                {"value": "sophisticated", "label": "Complex strategies and alternatives", "score": {"sophisticated": 2}}
            ]
        },
        {
            "id": "time_available",
            "question": "How much time can you dedicate to managing investments?",
            "type": "single_choice",
            "options": [
                {"value": 1, "label": "Just starting, need to learn (5+ hours/week)", "score": {"novice": 3}},
                {"value": 2, "label": "Limited time, want simple approach (1-2 hours/week)", "score": {"mid_career": 3}},
                {"value": 3, "label": "Significant time for active management (5+ hours/week)", "score": {"sophisticated": 3}}
            ]
        }
    ]
    
    def calculate_persona_scores(self, answers: Dict[str, Any]) -> Dict[str, float]:
        """Calculate scores for each persona based on questionnaire answers."""
        scores = {"novice": 0, "mid_career": 0, "sophisticated": 0}
        
        for question in self.RISK_QUESTIONNAIRE:
            q_id = question["id"]
            if q_id not in answers:
                continue
            
            user_answer = answers[q_id]
            
            # Find matching option
            for option in question["options"]:
                if option["value"] == user_answer or option["label"] == user_answer:
                    # Add scores
                    for persona, score in option.get("score", {}).items():
                        scores[persona] += score
                    break
        
        return scores
    
    def detect_persona(self, 
                      questionnaire_answers: Optional[Dict] = None,
                      portfolio_size: Optional[float] = None,
                      experience_years: Optional[float] = None,
                      risk_tolerance: Optional[str] = None) -> str:
        """
        Detect user persona.
        
        Priority:
        1. Questionnaire (if provided)
        2. Portfolio size + experience (if provided)
        3. Default to mid_career
        """
        
        if questionnaire_answers:
            scores = self.calculate_persona_scores(questionnaire_answers)
            # Return persona with highest score
            max_persona = max(scores, key=scores.get)
            
            # Map short names to full keys
            persona_map = {
                "novice": "novice_nisha",
                "mid_career": "mid_career_mohit",
                "sophisticated": "sophisticated_sanjay"
            }
            
            return persona_map[max_persona]
        
        # Fallback to heuristics
        if portfolio_size is not None or experience_years is not None:
            portfolio_size = portfolio_size or 0
            experience_years = experience_years or 0
            
            # Simple heuristic rules
            if experience_years < 2 or portfolio_size < 500000:
                return "novice_nisha"
            elif experience_years > 10 and portfolio_size > 3000000:
                return "sophisticated_sanjay"
            else:
                return "mid_career_mohit"
        
        # Default
        return "mid_career_mohit"
    
    def get_persona_profile(self, persona_key: str) -> Dict[str, Any]:
        """Get complete persona profile."""
        return self.PERSONAS.get(persona_key, self.PERSONAS["mid_career_mohit"])
    
    def get_response_adaptation_prompt(self, persona_key: str) -> str:
        """Get prompt instructions for adapting responses to persona."""
        persona = self.get_persona_profile(persona_key)
        style = persona["response_style"]
        
        if persona_key == "novice_nisha":
            return f"""
ADAPT FOR BEGINNER INVESTOR:
- Use SIMPLE language (avoid jargon like "P/E ratio" without explanation)
- Provide DETAILED explanations (explain WHY, not just WHAT)
- Include MANY examples ("For instance...", "Think of it like...")
- Be EDUCATIONAL (teach concepts)
- Tone: Supportive, patient, encouraging
- Add glossary of any financial terms used
- Use analogies and metaphors
- Highlight risks prominently
- Suggest conservative, proven investments
- Explain step-by-step action plans

Example transformation:
❌ "P/E of 25 indicates premium valuation"
✅ "P/E (Price-to-Earnings) ratio is 25, which means investors are paying ₹25 
   for every ₹1 of company earnings. Think of it like paying 25 years of 
   profits upfront. A P/E above 20 is generally considered high, meaning 
   the stock is expensive. However, high P/E can be justified if the 
   company is growing fast."
"""
        
        elif persona_key == "mid_career_mohit":
            return f"""
ADAPT FOR INTERMEDIATE INVESTOR:
- Use MODERATE complexity (financial terms OK, but explain advanced concepts)
- Provide CONCISE explanations (get to the point)
- Include FEW examples (only when needed)
- Be PROFESSIONAL and efficient
- Tone: Business-like, respectful of their time
- Focus on tax optimization and portfolio efficiency
- Highlight time-saving insights
- Provide clear action items
- Mention both growth and risk management

Example transformation:
✅ "P/E of 25 is above sector average of 20, indicating premium valuation. 
   Justified by ROE of 35% and strong growth trajectory. Consider for 
   long-term holding. Tax note: Holding >1 year qualifies for LTCG 
   (12.5% vs 20% STCG)."
"""
        
        else:  # sophisticated_sanjay
            return f"""
ADAPT FOR EXPERT INVESTOR:
- Use ADVANCED complexity (technical jargon expected)
- Provide MINIMAL explanations (they know the basics)
- Include RARE examples (assume knowledge)
- Be INSTITUTIONAL in tone
- Tone: Peer-to-peer, analytical, data-heavy
- Focus on alpha generation and sophisticated metrics
- Include statistical significance
- Mention hedging strategies
- Discuss relative value and factor exposures
- Provide contrarian insights

Example transformation:
✅ "Trading at 25x NTM earnings (15% premium to sector). Justified by 
   ROIC of 35% (2σ above sector), sustainable competitive advantage in 
   oligopolistic market structure. Beta-adjusted expected return: 
   18% p.a. Consider pair trade: long this, short sector ETF for 
   alpha isolation. Vol surface suggests 20% IV, positioning for 
   earnings vol expansion."
"""
        
        return ""
    
    def save_user_profile(self, user_id: str, persona_key: str, answers: Dict):
        """Save user profile for future sessions."""
        profile = {
            "user_id": user_id,
            "persona": persona_key,
            "detected_at": str(datetime.now()),
            "questionnaire_answers": answers,
            "persona_profile": self.get_persona_profile(persona_key)
        }
        
        # In production, save to database
        # For now, save to JSON
        filename = f"user_profiles/{user_id}.json"
        import os
        os.makedirs("user_profiles", exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump(profile, f, indent=2, default=str)
        
        return profile


from datetime import datetime


def demo_persona_detection():
    """Demo the persona detection system."""
    detector = PersonaDetector()
    
    print("=" * 70)
    print("PERSONA DETECTION DEMO")
    print("=" * 70)
    
    # Test Case 1: Novice Nisha
    print("\n📝 Test Case 1: Beginner Investor")
    answers_novice = {
        "experience": 0,
        "portfolio_size": 100000,
        "investment_knowledge": 1,
        "volatility_comfort": 1,
        "investment_goal": "learning",
        "time_available": 1
    }
    
    persona = detector.detect_persona(questionnaire_answers=answers_novice)
    profile = detector.get_persona_profile(persona)
    print(f"   Detected: {profile['name']}")
    print(f"   Description: {profile['description']}")
    print(f"   Response Style: {profile['response_style']['complexity']} complexity")
    
    # Test Case 2: Mid-Career Mohit
    print("\n📝 Test Case 2: Intermediate Investor")
    answers_mid = {
        "experience": 5,
        "portfolio_size": 1000000,
        "investment_knowledge": 3,
        "volatility_comfort": 3,
        "investment_goal": "retirement",
        "time_available": 2
    }
    
    persona = detector.detect_persona(questionnaire_answers=answers_mid)
    profile = detector.get_persona_profile(persona)
    print(f"   Detected: {profile['name']}")
    print(f"   Description: {profile['description']}")
    print(f"   Response Style: {profile['response_style']['complexity']} complexity")
    
    # Test Case 3: Sophisticated Sanjay
    print("\n📝 Test Case 3: Expert Investor")
    answers_expert = {
        "experience": 15,
        "portfolio_size": 15000000,
        "investment_knowledge": 5,
        "volatility_comfort": 5,
        "investment_goal": "alpha",
        "time_available": 3
    }
    
    persona = detector.detect_persona(questionnaire_answers=answers_expert)
    profile = detector.get_persona_profile(persona)
    print(f"   Detected: {profile['name']}")
    print(f"   Description: {profile['description']}")
    print(f"   Response Style: {profile['response_style']['complexity']} complexity")
    
    print("\n" + "=" * 70)
    print("✅ Persona Detection Working!")
    print("=" * 70)


if __name__ == "__main__":
    demo_persona_detection()
