# 🚀 Quick Start Guide

## Launch in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set API Key
Create or edit `.env` file:
```
GEMINI_API_KEY=your_actual_api_key_here
```

### Step 3: Launch
```bash
streamlit run app_unified.py
```

**That's it!** Open http://localhost:8501 in your browser.

---

## First Time Use

### Option A: Stock Advisor (For Retail Investors)

1. Click **"Launch Stock Advisor"**
2. Click **"Start Questionnaire"** (detect your persona)
3. Answer 6 questions honestly
4. Enter stock tickers: `RELIANCE.NS`, `TCS.NS`
5. Click **"Run Multi-Agent Analysis"**
6. View results in 5 tabs:
   - **Executive Summary** - See visual sentiment gauge! 📊
   - **Ask Questions** - Chat with AI about the analysis 💬
   - **Agent Insights** - Individual agent findings
   - **Detailed Analysis** - Raw data
   - **Execution Log** - Audit trail

### Option B: Merchant Underwriting (For Risk Analysts)

1. Click **"Launch Merchant Underwriting"**
2. Enter merchant details in sidebar
3. Click **"Run Underwriting Assessment"**
4. Review risk assessment brief in <30 seconds
5. Download report for audit trail

---

## Key Features to Try

### 🎯 Stock Advisor:

**1. Visual Sentiment Gauge** (NEW!)
- Check Executive Summary tab
- See Plotly dial: Red (Bearish) → Gray (Neutral) → Green (Bullish)

**2. Chat Interface** (NEW!)
- Click "Ask Questions" tab
- Ask: "What does the P/E ratio mean?"
- Get persona-adapted answer with memory

**3. Guardrails** (NEW!)
- Try asking: "Should I buy RELIANCE?"
- Watch it get blocked (no definitive advice)
- Try off-topic: "What's the weather?"
- Watch it get blocked (stocks only)

**4. Persona Experiences**:
- **Novice**: Get educational glossary + simple explanations
- **Mid-Career**: Get professional + tax-optimized advice
- **Sophisticated**: Get advanced analytics + hedging strategies

---

## 🏢 Merchant Underwriting:

**1. Quick Test**:
- Company: "Test Merchant Pvt Ltd"
- Industry: "E-commerce"
- Click Run → Get assessment in <30 seconds

**2. Test Prohibited Business**:
- Change Industry to "Gambling"
- Run assessment
- See REJECT decision

**3. View Audit Trail**:
- Check "Audit Trail" tab
- See all agent execution logs
- Perfect for compliance

---

## 🧪 Want to Test Everything?

Follow detailed **TESTING_GUIDE.md** for:
- All 3 personas
- All features
- Edge cases
- Performance benchmarks

---

## 📚 Need More Info?

- **Overview**: README.md
- **Features**: FEATURES_COMPLETE.md  
- **PRD Alignment**: PRD_IMPLEMENTATION_STATUS.md
- **Persona System**: PERSONA_ADAPTATION.md
- **Testing**: TESTING_GUIDE.md
- **Complete Status**: PROJECT_COMPLETE.md

---

## 💡 Pro Tips

1. **Test all 3 personas** - See how responses adapt
2. **Try the chat** - Ask follow-up questions
3. **Test guardrails** - See safety features in action
4. **Check sentiment gauge** - Visual PRD feature
5. **Switch products** - Try both Stock Advisor & Underwriting

---

## ⚡ Speed Run (2 Minutes)

```bash
# 1. Install
pip install -r requirements.txt

# 2. Add API key to .env
echo "GEMINI_API_KEY=your_key" > .env

# 3. Run
streamlit run app_unified.py

# 4. In browser:
#    - Click "Launch Stock Advisor"
#    - Enter: RELIANCE.NS
#    - Click "Run Analysis"
#    - See sentiment gauge + results
```

**Done!** ✅

---

## 🆘 Troubleshooting

**Problem**: API Key Error  
**Solution**: Check .env file has `GEMINI_API_KEY=your_key`

**Problem**: Module Not Found  
**Solution**: Run `pip install -r requirements.txt`

**Problem**: Slow Analysis  
**Solution**: Normal for first run (model initialization)

**Problem**: Persona Not Detecting  
**Solution**: Answer all 6 questionnaire questions

---

## 📊 What You'll See

### Stock Advisor Dashboard:
```
┌─────────────────────────────────────┐
│ 📈 Multi-Agent Stock Advisor        │
├─────────────────────────────────────┤
│ [Your Persona Badge]                │
│                                     │
│ Tabs:                               │
│ ┌─────────────────────────────────┐│
│ │ 📊 Executive Summary            ││
│ │   📰 Sentiment Gauge (Plotly)   ││
│ │   [Analysis Text]               ││
│ │   📚 Glossary (if Novice)       ││
│ │   📊 Analytics (if Sophisticated││
│ │                                  ││
│ │ 💬 Ask Questions                ││
│ │   [Chat Interface]              ││
│ │                                  ││
│ │ 🤖 Agent Insights               ││
│ │ 📈 Detailed Analysis            ││
│ │ 🔍 Execution Log                ││
│ └─────────────────────────────────┘│
└─────────────────────────────────────┘
```

### Merchant Underwriting Dashboard:
```
┌─────────────────────────────────────┐
│ 🏢 Merchant Underwriting            │
├─────────────────────────────────────┤
│ Sidebar: [Input Form]              │
│                                     │
│ Main:                               │
│ ┌─────────────────────────────────┐│
│ │ 🎯 Risk Assessment Brief        ││
│ │   Decision: APPROVE/REJECT      ││
│ │   Risk: LOW/MEDIUM/HIGH/CRITICAL││
│ │   Time: <30 seconds             ││
│ │                                  ││
│ │ [Executive Summary]             ││
│ │ [Red Flags]                     ││
│ │ [Recommendations]               ││
│ └─────────────────────────────────┘│
└─────────────────────────────────────┘
```

---

## 🎯 Success Indicators

You'll know it's working when:

✅ Product selector shows 2 cards  
✅ Persona questionnaire appears  
✅ Sentiment gauge displays (Plotly dial)  
✅ Chat interface responds  
✅ Guardrails block inappropriate queries  
✅ Analysis completes <60 seconds (Stock)  
✅ Assessment completes <30 seconds (Underwriting)  

---

## 🎉 You're Ready!

Explore both products, test all features, and see the AI in action.

**Need help?** Check the full documentation in the repo.

**Ready to demo?** Follow TESTING_GUIDE.md

---

**Happy Testing!** 🚀
