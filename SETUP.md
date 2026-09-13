# 🛠️ Setup Guide - Get Running in 5 Minutes

## ✅ What You Need

### 1. **Gemini API Key** (FREE)
- Go to: https://aistudio.google.com/app/apikey
- Click "Create API Key"
- Copy the key (starts with `AIza...`)
- **Cost**: Free tier includes generous limits (15 RPM, 1 million tokens/min)

### 2. **Python 3.8+**
- Check: `python --version`
- If not installed: Download from https://www.python.org/downloads/

---

## 🚀 Installation Steps

### Step 1: Install Dependencies
```bash
# In your project directory
cd "c:\AI Portfolio Advisor"

# Install all required packages
pip install -r requirements.txt
```

**Packages that will be installed:**
- `streamlit` - Web UI framework
- `yfinance` - Stock data from Yahoo Finance
- `google-genai` - Gemini API client
- `python-dotenv` - Environment variable management
- `pandas`, `numpy` - Data processing
- `chromadb` - Vector database for RAG
- `sentence-transformers` - Embeddings
- `plotly` - Sentiment gauge visualization
- Others for evals and fine-tuning

**Installation time**: ~2-3 minutes

---

### Step 2: Configure API Key

**Option A: Create .env file (Recommended)**
```bash
# Create .env file in project root
echo GEMINI_API_KEY=your_actual_api_key_here > .env
```

**Option B: Edit .env file manually**
1. Copy `.env.example` to `.env`
2. Open `.env` in any text editor
3. Replace `your_gemini_api_key_here` with your actual key

**Your .env should look like:**
```
GEMINI_API_KEY=AIzaSyC1234567890abcdefghijklmnopqrstuvw
```

⚠️ **Important**: Don't commit `.env` to git (it's already in .gitignore)

---

### Step 3: Launch the App
```bash
streamlit run app_unified.py
```

**What happens:**
- Streamlit starts a local web server
- Opens browser automatically at http://localhost:8501
- You'll see the unified dashboard with 2 product cards

**If browser doesn't open**, manually go to: http://localhost:8501

---

## ✅ Verify It's Working

### Quick Test (2 minutes):

1. **See the Dashboard**
   - [ ] Two cards appear: "Stock Advisor" and "Merchant Underwriting"

2. **Test Stock Advisor**
   - [ ] Click "Launch Stock Advisor"
   - [ ] Click "🚀 Start Questionnaire"
   - [ ] Answer 6 questions
   - [ ] Enter ticker: `RELIANCE.NS`
   - [ ] Click "Run Multi-Agent Analysis"
   - [ ] Wait ~30-60 seconds
   - [ ] See results with sentiment gauge ✅

3. **Test Chat**
   - [ ] Click "💬 Ask Questions" tab
   - [ ] Ask: "What is P/E ratio?"
   - [ ] Get answer ✅

4. **Test Merchant Underwriting**
   - [ ] Go back to dashboard
   - [ ] Click "Launch Merchant Underwriting"
   - [ ] Fill in test merchant data
   - [ ] Click "Run Underwriting Assessment"
   - [ ] Get results in <30 seconds ✅

---

## 🐛 Troubleshooting

### Problem 1: "GEMINI_API_KEY not found"
**Solution:**
```bash
# Check if .env file exists
ls .env

# Check contents (don't share the actual key!)
cat .env

# Make sure it's in the project root directory
# Should be at: c:\AI Portfolio Advisor\.env
```

### Problem 2: "ModuleNotFoundError"
**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install specific missing package
pip install streamlit
pip install google-genai
```

### Problem 3: "API Key Invalid"
**Solution:**
- Go to https://aistudio.google.com/app/apikey
- Check if API key is still active
- Create a new one if needed
- Update .env file with new key

### Problem 4: Port 8501 Already in Use
**Solution:**
```bash
# Run on different port
streamlit run app_unified.py --server.port 8502
```

### Problem 5: "No module named 'agents'"
**Solution:**
```bash
# Make sure you're in the project directory
cd "c:\AI Portfolio Advisor"

# Then run
streamlit run app_unified.py
```

### Problem 6: Slow Performance
**Solution:**
- First run is slower (downloads models)
- Subsequent runs are faster
- Stock analysis: expect 30-60 seconds
- Merchant underwriting: expect 20-30 seconds

---

## 📦 What Gets Downloaded (First Run)

When you first run the app:
1. **Sentence Transformers** (~500MB) - For embeddings
2. **ChromaDB data** - Vector database
3. **Model caches** - Gemini API responses

**Storage needed**: ~1-2GB for all dependencies and caches

---

## 🔧 Optional: Advanced Setup

### For Development:
```bash
# Install dev dependencies
pip install pytest black flake8 mypy

# Run tests
pytest scripts/

# Format code
black .
```

### For Production:
```bash
# Use virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Set production API key
echo GEMINI_API_KEY=prod_key > .env
```

---

## 🌐 Network Requirements

The app needs internet access for:
- **Yahoo Finance API** - Stock data (free, no key needed)
- **Google Gemini API** - AI responses
- **Streamlit** - UI framework

**Ports used:**
- `8501` - Default Streamlit port
- `443` - HTTPS for API calls

---

## 💰 API Costs

### Gemini 3.1 Pro Free Tier:
- **Requests**: 15 per minute
- **Tokens**: 1 million per minute
- **Daily**: 1,500 requests

### Typical Usage:
- **Stock Analysis**: ~50K tokens (50 analyses before limit)
- **Merchant Underwriting**: ~30K tokens (30 assessments before limit)
- **Chat Message**: ~5K tokens (200 messages before limit)

**For demo/portfolio**: Free tier is MORE than enough ✅

**For production**: Consider paid tier ($7/million tokens)

---

## ✅ System Requirements

### Minimum:
- **OS**: Windows 10/11, macOS 10.14+, or Linux
- **RAM**: 4GB
- **Storage**: 2GB free
- **Internet**: Broadband connection
- **Python**: 3.8+

### Recommended:
- **RAM**: 8GB+
- **Storage**: 5GB free
- **CPU**: Multi-core (for parallel agent execution)

---

## 📝 Environment Variables

**Required:**
```
GEMINI_API_KEY=your_api_key
```

**Optional:**
```
# For experiment tracking (if you uncomment in requirements.txt)
WANDB_API_KEY=your_wandb_key
MLFLOW_TRACKING_URI=your_mlflow_uri
```

---

## 🚀 Quick Start Commands

```bash
# Full setup from scratch
cd "c:\AI Portfolio Advisor"
pip install -r requirements.txt
echo GEMINI_API_KEY=AIza... > .env
streamlit run app_unified.py

# That's it! 🎉
```

---

## 📚 Next Steps

After setup:
1. **Read**: QUICK_START.md for usage guide
2. **Test**: Follow TESTING_GUIDE.md for comprehensive testing
3. **Explore**: Check PROJECT_COMPLETE.md for features
4. **Customize**: Modify agents/ for your use case

---

## 🆘 Still Stuck?

### Check These Files:
- `README.md` - Project overview
- `QUICK_START.md` - Usage guide
- `TESTING_GUIDE.md` - Feature testing
- `PROJECT_COMPLETE.md` - Complete documentation

### Common Issues:
1. **Wrong directory**: Make sure you're in `c:\AI Portfolio Advisor`
2. **Python version**: Must be 3.8 or higher
3. **API key**: Must start with `AIza` and be active
4. **Internet**: Required for APIs

---

## ✅ Setup Checklist

- [ ] Python 3.8+ installed
- [ ] Project downloaded/cloned
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Gemini API key obtained (free from aistudio.google.com)
- [ ] .env file created with API key
- [ ] App launches (`streamlit run app_unified.py`)
- [ ] Dashboard loads at localhost:8501
- [ ] Test analysis runs successfully

---

## 🎉 You're Ready!

Once all checks pass:
- Try Stock Advisor with different personas
- Test Merchant Underwriting
- Explore the chat interface
- Check the sentiment gauge
- Test the guardrails

**Enjoy your AI-powered fintech platform!** 🚀
