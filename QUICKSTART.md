# 🚀 Quick Start Guide
## Get Your Multi-Agent Portfolio Advisor Running in 5 Minutes

---

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Google Gemini API key ([Get one free here](https://aistudio.google.com/app/apikey))

---

## Step 1: Clone/Download the Project

```bash
# If using git
git clone <your-repo-url>
cd "AI Portfolio Advisor"

# Or download as ZIP and extract
```

---

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected packages**:
- streamlit (web UI)
- yfinance (market data)
- google-genai (AI agents)
- pandas, numpy (data processing)
- python-dotenv (environment variables)

---

## Step 3: Set Up API Key

### Option A: Using .env file (Recommended)

```bash
# Copy the example file
copy .env.example .env

# Edit .env file and add your API key
# On Windows: notepad .env
# On Mac/Linux: nano .env
```

In the .env file, replace:
```
GEMINI_API_KEY=your_api_key_here
```

with your actual key:
```
GEMINI_API_KEY=AIzaSyABC123...your-actual-key
```

### Option B: Set Environment Variable Directly

**Windows (PowerShell)**:
```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

**Mac/Linux**:
```bash
export GEMINI_API_KEY="your_api_key_here"
```

---

## Step 4: Test the System

```bash
python demo_agents.py
```

**What to expect**:
```
🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖
Multi-Agent Portfolio Advisor - System Test
🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖

✅ API key found

============================================================
Testing Financial Data Provider
============================================================
✅ Successfully fetched data for Reliance Industries Limited
   Current Price: ₹2500.00
   ...

✅ PASS - Data Provider
✅ PASS - Fundamental Agent
✅ PASS - Technical Agent
...

🎉 All systems operational! Ready for production.
```

**If tests fail**:
- ❌ API key error → Check your .env file
- ❌ Import error → Run `pip install -r requirements.txt` again
- ❌ Network error → Check internet connection

---

## Step 5: Run the Application

### Option A: Multi-Agent Version (Recommended)

```bash
streamlit run app_multiagent.py
```

### Option B: Simple Version (Original)

```bash
streamlit run app.py
```

---

## Step 6: Use the Application

1. **Browser Opens Automatically**
   - If not, go to: http://localhost:8501

2. **Configure Your Profile** (Left Sidebar)
   - Enter stock tickers (e.g., RELIANCE.NS, TCS.NS, INFY.NS)
   - Set investment corpus
   - Choose risk tolerance
   - Add preferences

3. **Run Analysis**
   - Click "🚀 Run Multi-Agent Analysis"
   - Wait 30-60 seconds
   - Explore results in tabs

4. **Download Report**
   - Click "📥 Download Full Report"
   - Get JSON file with complete analysis

---

## 🎯 Example Usage

### Scenario 1: Analyze Your Portfolio

**Input**:
```
Tickers: RELIANCE.NS, TCS.NS, HDFCBANK.NS
Corpus: ₹50,000
Risk: Moderate
```

**Output**:
- Multi-dimensional analysis of each stock
- Buy/Hold/Sell recommendations
- Risk assessment
- Rebalancing suggestions

### Scenario 2: Get Investment Ideas

**Input**:
```
Tickers: (leave empty)
Corpus: ₹1,00,000
Risk: Aggressive
Preferences: Focus on growth stocks in technology
```

**Output**:
- 3-5 stock recommendations
- Allocation percentages
- Risk-reward analysis
- Tax implications

---

## 🔧 Troubleshooting

### Problem: "GEMINI_API_KEY not found"
**Solution**: 
```bash
# Check if .env file exists
dir .env   # Windows
ls -la .env   # Mac/Linux

# Make sure it contains:
GEMINI_API_KEY=your_actual_key_here
```

### Problem: "No module named 'streamlit'"
**Solution**:
```bash
pip install -r requirements.txt --upgrade
```

### Problem: "Failed to fetch data for ticker"
**Solution**:
- Check ticker format: Use .NS for NSE, .BO for BSE
- Example: RELIANCE.NS (correct) vs RELIANCE (incorrect)
- Try with a different ticker to verify

### Problem: Page loads slowly
**Solution**:
- First run takes longer (downloading data)
- Subsequent runs are faster (caching)
- Analysis time depends on number of stocks (1 stock = ~20s, 5 stocks = ~60s)

### Problem: "Rate limit exceeded"
**Solution**:
- Free Gemini API has limits
- Wait a few minutes
- Consider upgrading to paid tier

---

## 📱 Using Different Versions

### Version 1: Simple (app.py)
- Single AI agent
- Basic analysis
- Faster (15-20 seconds)
- Good for quick checks

### Version 2: Multi-Agent (app_multiagent.py)
- 7+ specialized agents
- Comprehensive analysis
- Slower (30-60 seconds)
- Better for deep analysis

**Switch versions**:
```bash
# Stop current app (Ctrl+C)
# Run different version
streamlit run app.py          # Simple
streamlit run app_multiagent.py   # Multi-agent
```

---

## 🎓 Next Steps

### Learn More
- 📄 Read [README_MULTIAGENT.md](README_MULTIAGENT.md) for architecture details
- 📄 Read [PRD](docs/PRD_MultiAgent_Portfolio_Advisor.md) for product strategy
- 📄 Read [INTERVIEW_GUIDE.md](docs/INTERVIEW_GUIDE.md) for presentation tips

### Customize
- Add new agents in `agents/` folder
- Modify prompts in agent files
- Adjust UI in `app_multiagent.py`

### Deploy
- Deploy to Streamlit Cloud (free)
- Deploy to Heroku
- Deploy to your own server

---

## 💡 Tips for Best Experience

1. **Start with 1-2 stocks** to get familiar
2. **Try different risk profiles** to see how recommendations change
3. **Explore all tabs** (Summary, Agent Insights, Details, Logs)
4. **Download reports** to compare analyses over time
5. **Use specific tickers**: RELIANCE.NS, not just RELIANCE

---

## 📊 Sample Tickers to Try

### Large Cap (Stable)
- RELIANCE.NS (Reliance Industries)
- TCS.NS (Tata Consultancy Services)
- HDFCBANK.NS (HDFC Bank)
- INFY.NS (Infosys)

### Mid Cap (Growth)
- BAJAJFINSV.NS (Bajaj Finserv)
- DMART.NS (DMart)
- TATAPOWER.NS (Tata Power)

### Small Cap (High Risk)
- (Research current small caps as they change frequently)

---

## 🆘 Get Help

### Documentation
- [README.md](README.md) - Project overview
- [README_MULTIAGENT.md](README_MULTIAGENT.md) - Technical details
- [PRD](docs/PRD_MultiAgent_Portfolio_Advisor.md) - Product requirements

### Testing
```bash
python demo_agents.py   # Test all components
```

### Issues
- Check the terminal/console for error messages
- Look at Streamlit sidebar for status messages
- Verify internet connection (needed for market data)

---

## ✅ Success Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] API key set in .env file
- [ ] Test script passes (`python demo_agents.py`)
- [ ] App runs (`streamlit run app_multiagent.py`)
- [ ] Browser opens to localhost:8501
- [ ] Analysis completes successfully

**All checked?** 🎉 You're ready to use the Multi-Agent Portfolio Advisor!

---

## 🚀 Quick Command Reference

```bash
# Installation
pip install -r requirements.txt

# Testing
python demo_agents.py

# Run App
streamlit run app_multiagent.py    # Multi-agent version
streamlit run app.py                # Simple version

# Stop App
Ctrl + C    # In terminal

# Update Dependencies
pip install -r requirements.txt --upgrade
```

---

**Need help?** Check the full [README.md](README.md) or run `python demo_agents.py` to diagnose issues.

**Ready to present?** Check [INTERVIEW_GUIDE.md](docs/INTERVIEW_GUIDE.md) for interview tips.

Happy analyzing! 📈🤖
