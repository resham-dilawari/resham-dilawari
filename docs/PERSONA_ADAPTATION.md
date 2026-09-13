# 👤 Persona-Based Adaptation System

## Overview

The AI Portfolio Advisor now includes **persona-based adaptation** that automatically personalizes the experience for different investor types. The system detects user personas through an interactive questionnaire and adapts all recommendations, explanations, and features accordingly.

---

## 🎯 Three Investor Personas

### 1. 🌱 Novice Nisha (Beginner Investor)

**Profile:**
- Experience: 0-2 years
- Portfolio Size: ₹0-5 lakhs
- Risk Tolerance: Very Conservative to Conservative
- Investment Knowledge: Basic
- Goals: Learning, wealth creation, savings

**Characteristics:**
- Needs hand-holding and detailed explanations
- Uncomfortable with volatility
- Wants to learn investing fundamentals
- Prefers proven, stable investments
- Needs safety and security

**Adapted Features:**
- ✅ **Simple Language**: Avoids jargon, explains every term
- ✅ **Educational Mode**: Interactive glossary of financial terms
- ✅ **Detailed Explanations**: "WHY" behind every recommendation
- ✅ **Many Examples**: Analogies and real-world comparisons
- ✅ **Step-by-Step Guidance**: Clear action plans
- ✅ **Risk Warnings**: Prominent risk highlighting
- ✅ **Supportive Tone**: Patient, encouraging, non-judgmental

**Example Output:**
```
P/E (Price-to-Earnings) ratio is 25, which means investors are paying ₹25 
for every ₹1 of company earnings. Think of it like paying 25 years of 
profits upfront. A P/E above 20 is generally considered high, meaning 
the stock is expensive. However, high P/E can be justified if the 
company is growing fast.
```

---

### 2. 💼 Mid-Career Mohit (Intermediate Investor)

**Profile:**
- Experience: 3-10 years
- Portfolio Size: ₹5-30 lakhs
- Risk Tolerance: Moderate to Moderate-Aggressive
- Investment Knowledge: Intermediate
- Goals: Retirement, tax saving, wealth creation, children's education

**Characteristics:**
- Has basic investment knowledge
- Time-constrained professional
- Wants efficiency and optimization
- Focuses on long-term wealth building
- Tax-conscious

**Adapted Features:**
- ✅ **Moderate Complexity**: Financial terms OK, advanced concepts explained
- ✅ **Concise Explanations**: Gets to the point quickly
- ✅ **Professional Tone**: Business-like, respectful of time
- ✅ **Tax Optimization**: Highlights LTCG/STCG implications
- ✅ **Time-Saving Insights**: Quick wins and efficient strategies
- ✅ **Clear Action Items**: Practical, implementable steps
- ✅ **Balanced View**: Growth AND risk management

**Example Output:**
```
P/E of 25 is above sector average of 20, indicating premium valuation. 
Justified by ROE of 35% and strong growth trajectory. Consider for 
long-term holding. Tax note: Holding >1 year qualifies for LTCG 
(12.5% vs 20% STCG).
```

---

### 3. 🎓 Sophisticated Sanjay (Expert Investor)

**Profile:**
- Experience: 10+ years
- Portfolio Size: ₹30 lakhs+
- Risk Tolerance: Aggressive to Very Aggressive
- Investment Knowledge: Advanced (professional finance background)
- Goals: Alpha generation, wealth preservation, alternative investments

**Characteristics:**
- Deep financial expertise
- Comfortable with complex strategies
- Seeks institutional-grade insights
- Focuses on alpha generation
- Wants advanced analytics

**Adapted Features:**
- ✅ **Advanced Complexity**: Technical jargon expected
- ✅ **Advanced Analytics Dashboard**: Factor analysis, alpha decomposition
- ✅ **Minimal Explanations**: Assumes knowledge of basics
- ✅ **Institutional Tone**: Peer-to-peer, analytical, data-heavy
- ✅ **Statistical Significance**: P-values, confidence intervals
- ✅ **Hedging Strategies**: Options, pair trades, factor exposures
- ✅ **Contrarian Insights**: Beyond-obvious opportunities
- ✅ **Relative Value Analysis**: Vs benchmarks and peers

**Example Output:**
```
Trading at 25x NTM earnings (15% premium to sector). Justified by 
ROIC of 35% (2σ above sector), sustainable competitive advantage in 
oligopolistic market structure. Beta-adjusted expected return: 
18% p.a. Consider pair trade: long this, short sector ETF for 
alpha isolation. Vol surface suggests 20% IV, positioning for 
earnings vol expansion.
```

---

## 📋 Risk Questionnaire

### Automatic Persona Detection

The system uses a **6-question interactive questionnaire** to detect user persona:

1. **Investment Experience**
   - <1 year, 1-2 years, 3-7 years, 8-10 years, 10+ years

2. **Portfolio Size**
   - <₹2L, ₹2-5L, ₹5-15L, ₹15-30L, ₹30L-1Cr, >₹1Cr

3. **Investment Knowledge**
   - Beginner, Basic, Intermediate, Advanced, Expert

4. **Volatility Comfort**
   - "If your ₹1L investment dropped to ₹70K in a month, you would:"
   - Panic and sell, Feel uncomfortable, Feel concerned, See as normal, See as buying opportunity

5. **Investment Goals**
   - Learning, Safe savings, Wealth creation, Retirement, Beat market, Complex strategies

6. **Time Available**
   - Just starting (5+ hrs/week), Limited time (1-2 hrs/week), Active management (5+ hrs/week)

### Scoring Algorithm

Each answer contributes points to one or more personas. The persona with the highest score is selected.

**Example:**
```python
Answers: {
    experience: 0 years (+3 Novice),
    portfolio: ₹1L (+3 Novice),
    knowledge: Beginner (+3 Novice),
    volatility: Would panic (+3 Novice),
    goal: Learning (+3 Novice),
    time: Just starting (+3 Novice)
}
Total Score: Novice=18, Mid-Career=0, Sophisticated=0
→ Detected: Novice Nisha ✓
```

---

## 🎨 Feature Adaptations

### 1️⃣ Educational Mode (Novice Nisha)

**Automatic Features:**
- ✅ **Financial Glossary**: Explains every term found in analysis
- ✅ **Expanded Definitions**: Click to see detailed explanations
- ✅ **Real-World Analogies**: Makes concepts relatable
- ✅ **Step-by-Step Guidance**: Clear action plans

**Example Glossary Entry:**
```
💡 P/E Ratio
Price-to-Earnings ratio. Shows how much investors pay for each ₹1 
of company earnings. Lower is generally cheaper.

💡 Beta
Measures stock volatility vs market. Beta > 1 = more volatile, 
Beta < 1 = less volatile than market.

💡 Sharpe Ratio
Risk-adjusted return measure. Higher is better. Above 1 is good, 
above 2 is excellent.
```

### 2️⃣ Standard Experience (Mid-Career Mohit)

**Balanced Approach:**
- Professional, concise analysis
- Tax optimization highlights
- Time-efficient recommendations
- Clear action items
- Both growth and risk management

### 3️⃣ Advanced Analytics Dashboard (Sophisticated Sanjay)

**Institutional-Grade Features:**

#### **Alpha & Factor Analysis**
```
Factor Exposures:
- Size Factor: Medium cap tilt (+0.3 std dev)
- Value Factor: Neutral (0.0)
- Momentum Factor: Positive (+0.5 std dev)
- Quality Factor: High quality bias (+0.7 std dev)

Alpha Decomposition:
- Security Selection: +2.3% annualized
- Sector Allocation: +0.8% annualized
- Market Timing: -0.2% annualized
- Net Alpha: +2.9% vs Nifty 50
```

#### **Risk Decomposition**
```
Systematic Risk: 68% of total variance
- Market Beta: 1.12
- Sector Exposures: High IT (35%), Finance (25%)

Idiosyncratic Risk: 32% of total variance
- Stock-specific volatility
- Can be reduced via diversification

Tail Risk: 5th percentile loss = -18%
```

#### **Hedging Strategies**
```
1. Index Put Options
   - Buy Nifty 50 puts at 95% current level
   - Cost: ~0.8% of portfolio
   - Protection: Limits downside to -5%

2. Sector Rotation
   - Reduce IT exposure by 10%
   - Increase defensive (FMCG, Pharma) by 10%
   - Lower beta from 1.12 to 1.05

3. Pair Trade Opportunities
   - Long: INFY vs Short: TCS
   - Expected spread reversion: 5-8% over 3 months
```

#### **Statistical Significance**
```
Performance vs Benchmark:
- t-statistic: 2.3 (p-value < 0.05) ✅
- Statistically significant outperformance

Sharpe Ratio Confidence:
- Point estimate: 1.35
- 95% CI: [1.12, 1.58]

Information Ratio: 0.85
```

---

## 🔧 Technical Implementation

### Architecture

```
User Input
    ↓
Risk Questionnaire (6 questions)
    ↓
Persona Detector
    ↓
Scoring Algorithm
    ↓
Persona Selection
    ↓
┌─────────────────────────────────────┐
│  Novice    Mid-Career  Sophisticated │
│  Nisha        Mohit        Sanjay    │
└─────────────────────────────────────┘
    ↓
Feature Activation:
- Educational Mode (Novice)
- Standard Experience (Mid-Career)
- Advanced Analytics (Sophisticated)
    ↓
Prompt Adaptation:
- Orchestrator receives persona context
- LLM adapts language/complexity
- Response transformed per persona
    ↓
UI Customization:
- Glossary (Novice)
- Concise view (Mid-Career)
- Analytics dashboard (Sophisticated)
```

### Code Structure

```
persona_detector.py
├── PersonaDetector class
│   ├── PERSONAS (3 persona definitions)
│   ├── RISK_QUESTIONNAIRE (6 questions)
│   ├── calculate_persona_scores()
│   ├── detect_persona()
│   ├── get_persona_profile()
│   └── get_response_adaptation_prompt()
│
app_multiagent.py
├── Session state management
├── render_risk_questionnaire()
├── render_persona_badge()
├── render_educational_glossary()
├── render_advanced_analytics()
├── adapt_response_for_persona()
│
agents/orchestrator.py
├── _synthesize_insights() [updated]
│   └── Includes persona_adaptation in prompt
├── _analyze_portfolio() [updated]
└── _suggest_investments() [updated]
```

### Persona Adaptation Flow

1. **Questionnaire Completion**
   ```python
   answers = {
       "experience": 0,
       "portfolio_size": 100000,
       "investment_knowledge": 1,
       # ...
   }
   persona = detector.detect_persona(questionnaire_answers=answers)
   # Returns: "novice_nisha"
   ```

2. **Prompt Generation**
   ```python
   adaptation_prompt = detector.get_response_adaptation_prompt("novice_nisha")
   # Returns detailed instructions for LLM to adapt language
   ```

3. **Orchestrator Integration**
   ```python
   context = {
       "user_profile": {
           "persona": "novice_nisha",
           "persona_adaptation": adaptation_prompt
       }
   }
   # Orchestrator includes this in synthesis prompt
   ```

4. **UI Rendering**
   ```python
   if persona == "novice_nisha":
       render_educational_glossary(response_text)
   elif persona == "sophisticated_sanjay":
       render_advanced_analytics(results)
   ```

---

## 📊 Before vs After Comparison

### Example: P/E Ratio Explanation

**❌ Before (One-Size-Fits-All):**
```
P/E ratio is 25, indicating premium valuation.
```

**✅ After (Persona-Adapted):**

**Novice Nisha:**
```
📚 Beginner-Friendly Explanation:

P/E (Price-to-Earnings) ratio is 25, which means investors are 
paying ₹25 for every ₹1 of company earnings. Think of it like 
paying 25 years of profits upfront.

💡 What does this mean?
- P/E below 15: Generally cheap
- P/E 15-20: Fair value
- P/E above 20: Expensive (what we have here)

🤔 But wait! High P/E isn't always bad. Fast-growing companies 
often have high P/E because investors believe future earnings 
will be much higher.

💡 Key Takeaway: This stock is expensive today but might be 
worth it if the company grows fast.
```

**Mid-Career Mohit:**
```
💼 Professional Analysis:

P/E of 25 is above sector average of 20, indicating 15% premium. 
Justified by ROE of 35% and strong growth trajectory. PEG ratio 
of 1.2 suggests reasonable valuation given growth.

⏰ Action: Consider for long-term holding. Hold >1 year for LTCG 
tax benefit (12.5% vs 20% STCG).
```

**Sophisticated Sanjay:**
```
🎓 Advanced Analysis:

Trading at 25x NTM earnings (15% premium to sector median). 
Forward P/E compression to 21x implies 18% EPS CAGR. Justified 
by ROIC of 35% (2σ above sector), sustainable moat in oligopoly.

Beta-adjusted expected return: 18% p.a. (vs sector 12%).
t-stat: 2.1 (p<0.05). Consider overweight vs sector ETF for 
alpha capture.

📊 Alpha Opportunity: Pair trade long this vs short sector 
index for pure alpha isolation.
```

---

## 🚀 Usage Guide

### For End Users

1. **First Time Use:**
   - Launch app: `streamlit run app_multiagent.py`
   - Click "🚀 Start Questionnaire" in sidebar
   - Answer 6 questions honestly
   - System detects your persona automatically

2. **Persona Badge:**
   - Your persona appears at top of sidebar
   - Shows icon and description
   - Can retake questionnaire anytime

3. **Persona-Specific Features:**
   - **Novice**: Educational mode auto-enabled (glossary)
   - **Mid-Career**: Standard experience (balanced)
   - **Sophisticated**: Advanced analytics auto-enabled

4. **Changing Persona:**
   - Click "🔄 Retake Questionnaire"
   - Answer differently
   - New persona detected immediately

### For Developers

1. **Testing Different Personas:**
   ```python
   from persona_detector import PersonaDetector
   
   detector = PersonaDetector()
   
   # Test Novice
   novice_answers = {"experience": 0, "portfolio_size": 100000, ...}
   persona = detector.detect_persona(questionnaire_answers=novice_answers)
   
   # Test Sophisticated
   expert_answers = {"experience": 15, "portfolio_size": 15000000, ...}
   persona = detector.detect_persona(questionnaire_answers=expert_answers)
   ```

2. **Accessing Adaptation Prompts:**
   ```python
   prompt = detector.get_response_adaptation_prompt("novice_nisha")
   # Use in your LLM calls
   ```

3. **Extending Personas:**
   - Add new persona to `PersonaDetector.PERSONAS`
   - Update questionnaire scoring
   - Create new feature renderers

---

## 🎯 Benefits

### For Users

1. **Novice Nisha:**
   - ✅ Less intimidated by financial jargon
   - ✅ Learns while getting advice
   - ✅ Makes informed decisions
   - ✅ Builds confidence gradually

2. **Mid-Career Mohit:**
   - ✅ Saves time with concise insights
   - ✅ Tax-optimized strategies
   - ✅ Professional-grade analysis
   - ✅ Actionable recommendations

3. **Sophisticated Sanjay:**
   - ✅ Institutional-grade analytics
   - ✅ Advanced strategies (hedging, pair trades)
   - ✅ Statistical rigor
   - ✅ Alpha generation opportunities

### For Product

1. **Higher Engagement:**
   - Personalized experiences increase retention
   - Users feel understood
   - Appropriate complexity level

2. **Better Outcomes:**
   - Novices learn and grow
   - Intermediates optimize efficiently
   - Experts find actionable alpha

3. **Differentiation:**
   - Unique feature vs competitors
   - Shows AI sophistication
   - Demonstrates UX thoughtfulness

4. **Portfolio Project Impact:**
   - 🎯 **PM Role Showcase**: Demonstrates user segmentation
   - 🎯 **AI Implementation**: Advanced prompt engineering
   - 🎯 **UX Design**: Persona-based experiences
   - 🎯 **Technical Depth**: Multi-modal adaptation system

---

## 📈 Future Enhancements

### Planned Features

1. **Dynamic Persona Evolution:**
   - Track user behavior over time
   - Automatically upgrade persona (Novice → Mid-Career)
   - Gradual complexity increase

2. **Learning Path:**
   - For Novice: Structured learning modules
   - Progress tracking
   - Achievement badges

3. **Customization:**
   - Manual persona override
   - Feature toggle (turn off glossary)
   - Custom complexity slider

4. **Analytics:**
   - Track which persona uses which features
   - A/B test different adaptations
   - Optimize conversion by persona

5. **More Personas:**
   - Retiree (income-focused)
   - Trader (short-term, active)
   - ESG Investor (values-based)

---

## 🧪 Testing

### Manual Testing

```bash
# Run demo
python persona_detector.py

# Output:
# Test Case 1: Beginner Investor → Novice Nisha ✓
# Test Case 2: Intermediate Investor → Mid-Career Mohit ✓
# Test Case 3: Expert Investor → Sophisticated Sanjay ✓
```

### Integration Testing

```bash
# Run app
streamlit run app_multiagent.py

# Test flow:
1. Click "Start Questionnaire"
2. Answer as beginner → Check educational mode enabled
3. Retake questionnaire
4. Answer as expert → Check advanced analytics enabled
```

---

## 📚 Related Documentation

- [Main README](../README.md) - Project overview
- [Multi-Agent Architecture](ARCHITECTURE.md) - System design
- [Prompts Documentation](PROMPTS.md) - All agent prompts
- [Evaluation Framework](EVALUATION_FRAMEWORK.md) - Testing approach

---

## 🎉 Summary

The persona-based adaptation system transforms the AI Portfolio Advisor from a **one-size-fits-all** tool into a **personalized financial companion** that meets users where they are.

**Key Achievements:**
- ✅ 3 distinct personas with clear characteristics
- ✅ Automatic detection via 6-question questionnaire
- ✅ Educational mode with interactive glossary
- ✅ Advanced analytics dashboard
- ✅ Prompt-level response adaptation
- ✅ UI-level feature customization
- ✅ Seamless multi-agent integration

**Impact:**
- 🎯 Better user experience for ALL skill levels
- 🎯 Higher engagement and retention
- 🎯 Learning opportunity for novices
- 🎯 Alpha insights for experts
- 🎯 Strong portfolio project differentiator

---

**Built with ❤️ for personalized financial advice**
