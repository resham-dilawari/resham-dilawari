# 🧪 Testing Guide - All Features & Personas

## Overview

This guide provides step-by-step testing procedures for **both products** across **all personas** and **all new PRD features**.

---

## 🎯 Testing Matrix

### Products to Test:
1. **Stock Advisor** (3 personas)
2. **Merchant Underwriting** (single user type)

### Features to Test:
1. ✅ Visual Sentiment Gauge (Plotly dial)
2. ✅ Chat Interface (conversational follow-ups)
3. ✅ Input Guardrails (query validation)
4. ✅ Output Guardrails (safety filters)
5. ✅ Gemini 1.5 Pro (model upgrade)
6. ✅ Persona-based adaptation
7. ✅ Educational mode (Novice)
8. ✅ Advanced analytics (Sophisticated)

---

## 📋 Test Execution Checklist

### ✅ Pre-Test Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Verify API key is set
# Check .env file has GEMINI_API_KEY

# 3. Launch unified dashboard
streamlit run app_unified.py
```

**Expected**: Dashboard shows 2 product cards

---

## 🧪 Test Suite 1: Stock Advisor - Novice Nisha

### Step 1: Product Selection
- [ ] Click "Launch Stock Advisor"
- [ ] **Expected**: Stock Advisor UI loads

### Step 2: Persona Detection
- [ ] Click "🚀 Start Questionnaire" in sidebar
- [ ] **Answer as Novice:**
  - Experience: <1 year
  - Portfolio: <₹2L
  - Knowledge: Beginner
  - Volatility: Would panic
  - Goal: Learning
  - Time: Just starting
- [ ] Click "Submit & Detect My Persona"
- [ ] **Expected**: 
  - ✅ Persona detected: "Novice Nisha"
  - 📚 Educational Mode auto-enabled

### Step 3: Run Analysis
- [ ] Enter tickers: `RELIANCE.NS`, `TCS.NS`
- [ ] Corpus: ₹100,000
- [ ] Risk: Moderate
- [ ] Click "Run Multi-Agent Analysis"
- [ ] **Expected**: Analysis completes in <60 seconds

### Step 4: Test Sentiment Gauge (NEW FEATURE)
- [ ] Check "Executive Summary" tab
- [ ] **Expected**: 
  - Visual Plotly gauge showing sentiment (-1 to +1)
  - Color-coded: Red (Bearish), Gray (Neutral), Green (Bullish)
  - Sentiment interpretation below gauge
- [ ] **Verify**: Gauge matches sentiment agent analysis

### Step 5: Test Persona Adaptation
- [ ] Read synthesis text in Executive Summary
- [ ] **Expected for Novice:**
  - 📚 Prefix: "Beginner-Friendly Explanation"
  - Simple language, no jargon
  - Many examples and analogies
  - Step-by-step guidance

### Step 6: Test Educational Glossary
- [ ] Scroll down in Executive Summary
- [ ] **Expected**: 
  - "📚 Financial Terms Glossary" section appears
  - Expandable terms with definitions
  - Terms like P/E, Beta, Sharpe Ratio explained

### Step 7: Test Chat Interface (NEW FEATURE)
- [ ] Click "💬 Ask Questions" tab
- [ ] **Test Valid Question**: "What does the P/E ratio mean?"
- [ ] Click "Ask"
- [ ] **Expected**:
  - Answer appears using context from analysis
  - Adapted for Novice (simple explanation)
  - Added to chat history

### Step 8: Test Input Guardrails (NEW FEATURE)
- [ ] In chat, enter: "Should I buy RELIANCE now?"
- [ ] Click "Ask"
- [ ] **Expected**:
  - ❌ Error: "We provide analysis, not definitive buy/sell advice"
  - Query blocked
  
- [ ] Enter: "What's the weather today?"
- [ ] Click "Ask"
- [ ] **Expected**:
  - ❌ Error: "Please ask questions about stocks only"
  - Query blocked

### Step 9: Test Output Guardrails (NEW FEATURE)
- [ ] Check any AI response
- [ ] **Expected**:
  - Contains disclaimer: "not financial advice"
  - No PII (emails, phone numbers)
  - No excessive confidence ("guaranteed", "definitely")

### Step 10: Download Report
- [ ] Click "Download Full Report"
- [ ] **Expected**: JSON file downloads with all analysis

---

## 🧪 Test Suite 2: Stock Advisor - Mid-Career Mohit

### Step 1: Reset Persona
- [ ] Click "🔄 Retake Questionnaire"
- [ ] **Answer as Mid-Career:**
  - Experience: 5 years
  - Portfolio: ₹10L
  - Knowledge: Intermediate
  - Volatility: Feel concerned but hold
  - Goal: Wealth creation
  - Time: Limited time (1-2 hrs/week)
- [ ] Submit
- [ ] **Expected**: "Mid-Career Mohit" detected

### Step 2: Run Analysis
- [ ] Same tickers: RELIANCE.NS, TCS.NS
- [ ] Run analysis

### Step 3: Verify Persona Adaptation
- [ ] Check Executive Summary
- [ ] **Expected for Mid-Career:**
  - 💼 Prefix: "Professional Analysis"
  - Concise, efficient format
  - Tax optimization highlighted (LTCG/STCG)
  - Clear action items

### Step 4: Test Chat with Mid-Career Persona
- [ ] Ask: "What's the tax impact of selling?"
- [ ] **Expected**:
  - Professional tone
  - Tax details (LTCG 12.5%, STCG 20%)
  - Concise answer

### Step 5: Verify NO Educational Glossary
- [ ] Check Executive Summary
- [ ] **Expected**: No glossary (not needed for intermediate)

---

## 🧪 Test Suite 3: Stock Advisor - Sophisticated Sanjay

### Step 1: Reset Persona
- [ ] Retake questionnaire
- [ ] **Answer as Sophisticated:**
  - Experience: 15+ years
  - Portfolio: >₹1Cr
  - Knowledge: Expert
  - Volatility: See as buying opportunity
  - Goal: Beat market consistently
  - Time: Active management (5+ hrs/week)
- [ ] Submit
- [ ] **Expected**: "Sophisticated Sanjay" detected
- [ ] **Expected**: Advanced Analytics auto-enabled

### Step 2: Run Analysis
- [ ] Same tickers
- [ ] Run analysis

### Step 3: Verify Advanced Analytics (PERSONA FEATURE)
- [ ] Check Executive Summary, scroll down
- [ ] **Expected**:
  - "📊 Advanced Analytics Dashboard" appears
  - Factor Analysis (Size, Value, Momentum, Quality)
  - Alpha Decomposition
  - Risk Decomposition (Systematic vs Idiosyncratic)
  - Hedging Strategies (Options, Pair Trades)
  - Statistical Significance (t-stats, p-values)

### Step 4: Verify Persona Adaptation
- [ ] **Expected for Sophisticated:**
  - 🎓 Prefix: "Advanced Analysis"
  - Technical jargon acceptable
  - Minimal hand-holding
  - Institutional-grade metrics

### Step 5: Test Chat with Sophisticated Persona
- [ ] Ask: "What's the beta-adjusted expected return?"
- [ ] **Expected**:
  - Technical, advanced answer
  - Statistical metrics
  - Assumes financial expertise

---

## 🧪 Test Suite 4: Sentiment Gauge Variations

### Test Different Sentiment Scenarios:

**Bullish Scenario:**
- [ ] If sentiment agent reports "Bullish" or "Positive"
- [ ] **Expected Gauge**: Green zone (0.3 to 1.0)
- [ ] **Label**: "🟢 BULLISH"

**Neutral Scenario:**
- [ ] If sentiment reports "Neutral" or "Mixed"
- [ ] **Expected Gauge**: Gray zone (-0.3 to 0.3)
- [ ] **Label**: "⚪ NEUTRAL"

**Bearish Scenario:**
- [ ] If sentiment reports "Bearish" or "Negative"
- [ ] **Expected Gauge**: Red zone (-1.0 to -0.3)
- [ ] **Label**: "🔴 BEARISH"

---

## 🧪 Test Suite 5: Merchant Underwriting

### Step 1: Product Selection
- [ ] From unified dashboard, click "Launch Merchant Underwriting"
- [ ] **Expected**: Underwriting UI loads

### Step 2: Enter Merchant Data
- [ ] **Company**: Test Merchant Pvt Ltd
- [ ] **Registration**: CIN123456789
- [ ] **Website**: https://test-merchant.com
- [ ] **Industry**: E-commerce
- [ ] **Country**: India
- [ ] **Directors**: John Doe, Jane Smith
- [ ] **Business Description**: Online retail platform
- [ ] **Financial Data**: 
  - Revenue: ₹10,00,000
  - Profit: ₹1,00,000
  - Assets: ₹5,00,000
- [ ] Click "Run Underwriting Assessment"

### Step 3: Verify Agent Execution
- [ ] **Expected**: 5 agents run in parallel
  - 🚨 Red Flag Agent
  - 📋 Business Model Agent
  - 💰 Financial Health Agent
  - 🔍 Sanctions & Watchlist Agent
  - 🎭 Orchestrator

### Step 4: Check Risk Assessment Brief
- [ ] Tab 1: "Risk Assessment Brief"
- [ ] **Expected**:
  - Decision badge (APPROVE/REJECT/etc.)
  - Risk level (LOW/MEDIUM/HIGH/CRITICAL)
  - Assessment time: <30 seconds
  - Executive summary

### Step 5: Check Agent Details
- [ ] Tab 2: "Agent Details"
- [ ] **Expected**: Individual findings from each agent
- [ ] Verify risk levels are color-coded

### Step 6: Test Prohibited Business
- [ ] Change Industry to: "Gambling"
- [ ] Run assessment
- [ ] **Expected**:
  - Business Model Agent flags as PROHIBITED
  - Overall decision: REJECT
  - Risk level: CRITICAL

### Step 7: Download Report
- [ ] Click "Download Risk Assessment Report"
- [ ] **Expected**: JSON file with audit trail

---

## 🧪 Test Suite 6: Guardrails Edge Cases

### Input Guardrails:

**Test 1: Empty Query**
- [ ] Leave question blank, click Ask
- [ ] **Expected**: "Query too short" error

**Test 2: Too Long Query**
- [ ] Enter 1500 character query
- [ ] **Expected**: "Query too long" error

**Test 3: Definitive Advice Requests**
- [ ] "Tell me to buy TCS"
- [ ] **Expected**: Blocked with rephrasing suggestion

**Test 4: Off-Topic Queries**
- [ ] "Who won the cricket match?"
- [ ] **Expected**: "Please ask about stocks only"

### Output Guardrails:

**Test 1: Missing Disclaimer**
- [ ] Check any AI response
- [ ] **Expected**: Disclaimer auto-added if missing

**Test 2: PII Detection** (Simulated)
- [ ] If response contained email/phone (shouldn't in normal use)
- [ ] **Expected**: Redacted as [EMAIL REDACTED], [PHONE REDACTED]

**Test 3: Excessive Confidence**
- [ ] If AI uses "guaranteed", "definitely", "100% sure"
- [ ] **Expected**: Softened to "likely", "probably", "confident"

---

## 🧪 Test Suite 7: Cross-Product Navigation

### Test 1: Switch Products
- [ ] From Stock Advisor, click "⬅️ Back to Product Selection"
- [ ] **Expected**: Returns to unified dashboard
- [ ] Click "Launch Merchant Underwriting"
- [ ] **Expected**: Loads underwriting without errors

### Test 2: Persona Persistence
- [ ] Detect persona in Stock Advisor
- [ ] Switch to Merchant Underwriting
- [ ] Switch back to Stock Advisor
- [ ] **Expected**: Persona still detected (session state preserved)

---

## 🧪 Test Suite 8: Analysis Modes

### Stock Analysis Only
- [ ] Select "Stock Analysis Only"
- [ ] Run analysis
- [ ] **Expected**: Only portfolio analysis agents run

### Risk Analytics Only
- [ ] Select "Risk Analytics Only"
- [ ] Run analysis
- [ ] **Expected**: Focus on risk metrics

### Investment Suggestions Only
- [ ] Select "Investment Suggestions Only"
- [ ] No tickers needed
- [ ] **Expected**: Research + Optimizer agents provide suggestions

### Full Advisory
- [ ] Select "Full Advisory"
- [ ] **Expected**: All agents run, both analysis + suggestions

---

## ✅ Pass/Fail Criteria

### Critical (Must Pass):
- [ ] All 3 personas detect correctly
- [ ] Sentiment gauge displays visual dial
- [ ] Chat interface works with memory
- [ ] Input guardrails block inappropriate queries
- [ ] Output guardrails add disclaimer
- [ ] Gemini 1.5 Pro is being used
- [ ] Both products launch without errors

### Important (Should Pass):
- [ ] Educational glossary appears for Novice
- [ ] Advanced analytics appears for Sophisticated
- [ ] Persona adaptation is visible in responses
- [ ] PII redaction works if triggered
- [ ] Merchant underwriting completes <30 seconds

### Nice-to-Have (Can Fail):
- [ ] Perfect sentiment score extraction
- [ ] 100% accurate hallucination detection
- [ ] All edge cases handled gracefully

---

## 🐛 Known Issues & Workarounds

### Issue 1: Sentiment Gauge Shows Neutral
**Cause**: Sentiment agent didn't provide clear Bullish/Bearish signal
**Workaround**: Manual score extraction logic defaults to 0.0 (neutral)
**Fix**: Enhance sentiment agent prompts

### Issue 2: Chat Answer Too Long
**Cause**: Orchestrator verbose response
**Workaround**: User can ask for shorter answer
**Fix**: Add max_tokens limit to _answer_followup_question

### Issue 3: Guardrails Slow
**Cause**: LLM-based validation takes 2-3 seconds
**Workaround**: Quick pattern-based checks run first
**Fix**: Cache common queries

---

## 📊 Test Results Template

```
Test Date: __________
Tester: __________

Stock Advisor - Novice Nisha:     ☐ PASS  ☐ FAIL
Stock Advisor - Mid-Career Mohit: ☐ PASS  ☐ FAIL
Stock Advisor - Sophisticated:    ☐ PASS  ☐ FAIL
Merchant Underwriting:            ☐ PASS  ☐ FAIL
Sentiment Gauge:                  ☐ PASS  ☐ FAIL
Chat Interface:                   ☐ PASS  ☐ FAIL
Input Guardrails:                 ☐ PASS  ☐ FAIL
Output Guardrails:                ☐ PASS  ☐ FAIL

Critical Issues Found: __________
Notes: __________
```

---

## 🚀 Quick Smoke Test (5 Minutes)

For rapid validation:

1. **Launch**: `streamlit run app_unified.py`
2. **Stock Advisor**: Click launch
3. **Persona**: Start questionnaire, answer as Novice
4. **Analyze**: RELIANCE.NS, TCS.NS → Run Analysis
5. **Verify**: 
   - Sentiment gauge appears ✅
   - Educational glossary appears ✅
6. **Chat**: Ask "What is P/E ratio?" → Gets answer ✅
7. **Guardrail**: Ask "Should I buy?" → Gets blocked ✅
8. **Switch**: Back to dashboard
9. **Underwriting**: Launch, enter test merchant → Run
10. **Verify**: Assessment completes <30s ✅

**If all 10 pass → System working!** ✅

---

## 📝 Testing Notes

### Environment:
- Python: 3.8+
- Streamlit: 1.30+
- Gemini API: 1.5 Pro
- OS: Windows/Mac/Linux

### Performance Benchmarks:
- Stock analysis: <60 seconds
- Merchant underwriting: <30 seconds
- Sentiment gauge render: <1 second
- Chat response: 3-5 seconds
- Guardrail validation: 1-3 seconds

---

## ✅ Sign-Off

All tests completed and documented.

**Status**: ☐ All Pass ☐ Partial Pass ☐ Fail  
**Date**: __________  
**Tester**: __________  
**Notes**: __________

---

**Ready for Production Demo** ✅
