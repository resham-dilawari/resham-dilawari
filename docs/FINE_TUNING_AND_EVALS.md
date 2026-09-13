# 🎯 Fine-Tuning and Evaluation Guide
## Multi-Agent Portfolio Advisor

---

## Table of Contents
1. [Fine-Tuning Strategy](#fine-tuning-strategy)
2. [Evaluation Framework](#evaluation-framework)
3. [Data Collection](#data-collection)
4. [Implementation Steps](#implementation-steps)
5. [Continuous Improvement Loop](#continuous-improvement-loop)

---

## 1. Fine-Tuning Strategy

### Why Fine-Tune?

**Current Approach**: Zero-shot prompting with Gemini 2.0
- ✅ Fast to implement
- ✅ No training data needed
- ❌ Generic responses
- ❌ May not capture Indian market nuances
- ❌ Inconsistent formatting

**With Fine-Tuning**:
- ✅ More accurate for Indian market specifics
- ✅ Consistent output format
- ✅ Better understanding of financial terminology
- ✅ Improved reasoning quality
- ✅ Lower inference costs (smaller model)

---

### What to Fine-Tune?

#### Option A: Fine-Tune Entire Agents ⭐ Recommended
Fine-tune each specialized agent separately:

```
🔍 Fundamental Agent → Fine-tuned on 1000+ fundamental analyses
📈 Technical Agent → Fine-tuned on 1000+ technical analyses  
📰 Sentiment Agent → Fine-tuned on 1000+ news sentiment analyses
⚠️ Risk Agent → Fine-tuned on 500+ risk assessments
... and so on
```

**Advantage**: Each agent becomes hyper-specialized

#### Option B: Fine-Tune Orchestrator Only
Keep specialized agents as-is, fine-tune only orchestrator for:
- Better conflict resolution
- Improved synthesis
- More coherent recommendations

#### Option C: Fine-Tune Base Model
Create one fine-tuned base model, use different prompts per agent

---

### Fine-Tuning Approaches

#### 1. **Supervised Fine-Tuning (SFT)**

**Data Format:**
```json
[
  {
    "input": "Analyze RELIANCE.NS fundamentals. P/E: 25.5, ROE: 12.3%, Debt/Equity: 0.45, Revenue Growth: 18%",
    "output": "**Fundamental Analysis - RELIANCE.NS**\n\n**Executive Summary:** Strong fundamentals with healthy growth, but slight valuation concern.\n\n**Financial Health (Score: 8/10)**\n- ROE of 12.3% indicates efficient capital use\n- Conservative debt management (D/E 0.45)\n- Strong revenue growth of 18% YoY\n\n**Valuation (Score: 6/10)**\n- P/E of 25.5 is above sector average of 22\n- Growth premium justified but limited upside\n\n**Rating: HOLD**\n**Confidence: HIGH**\n**Target Price: ₹2,300**"
  },
  // ... 1000+ examples
]
```

**How to Generate Training Data:**

1. **Manual Curation** (100-200 examples)
   - Use current system to generate analyses
   - Manually review and correct
   - Ensure high quality

2. **Synthetic Data Generation** (800+ examples)
   - Use GPT-4 or Claude to generate training pairs
   - Vary stock tickers, metrics, scenarios
   - Review samples for quality

3. **Real User Interactions** (ongoing)
   - Collect user feedback on recommendations
   - User-corrected analyses
   - Thumbs up/down ratings

---

#### 2. **Reinforcement Learning from Human Feedback (RLHF)**

**Process:**
```
1. Collect User Feedback
   ↓
2. Train Reward Model (what makes a good recommendation?)
   ↓
3. Fine-tune with RL (PPO algorithm)
   ↓
4. Deploy Improved Model
```

**User Feedback Collection:**
- Thumbs up/down on recommendations
- "Was this helpful?" ratings
- User comments on analyses
- Track if user follows recommendations

**Reward Signals:**
- Recommendation accuracy (did stock perform as predicted?)
- User satisfaction scores
- Engagement metrics (did user read full analysis?)

---

#### 3. **Parameter-Efficient Fine-Tuning (PEFT)**

Use **LoRA (Low-Rank Adaptation)** to fine-tune with minimal resources:

```python
from peft import LoraConfig, get_peft_model

# Configure LoRA
lora_config = LoraConfig(
    r=16,  # Low-rank dimension
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
)

# Apply to base model
model = get_peft_model(base_model, lora_config)

# Fine-tune (only 1-2% of parameters updated!)
```

**Advantages:**
- ✅ Fast training (hours vs days)
- ✅ Low memory requirements
- ✅ Easy to switch between different fine-tuned versions
- ✅ Can keep multiple agent versions

---

## 2. Evaluation Framework

### A. Quantitative Metrics

#### 1. **Recommendation Accuracy** (Primary Metric)

```python
def recommendation_accuracy(predictions, actuals, timeframe="1M"):
    """
    Evaluate if BUY/HOLD/SELL recommendations were correct.
    
    Args:
        predictions: List of recommendations with timestamps
        actuals: Actual stock performance over timeframe
        timeframe: "1W", "1M", "3M", "6M"
    
    Returns:
        accuracy, precision, recall, f1_score
    """
    correct = 0
    total = len(predictions)
    
    for pred in predictions:
        ticker = pred['ticker']
        recommendation = pred['rating']  # BUY/HOLD/SELL
        pred_date = pred['date']
        
        # Get actual performance
        actual_return = get_stock_return(ticker, pred_date, timeframe)
        
        # Define success criteria
        if recommendation == "BUY" and actual_return > 5%:
            correct += 1
        elif recommendation == "HOLD" and -5% <= actual_return <= 5%:
            correct += 1
        elif recommendation == "SELL" and actual_return < -5%:
            correct += 1
    
    return correct / total
```

**Target Metrics:**
- 1-Month Accuracy: >60% (vs 50% random baseline)
- 3-Month Accuracy: >55%
- 6-Month Accuracy: >50%

---

#### 2. **Risk-Adjusted Performance**

```python
def evaluate_portfolio_performance(recommendations, actual_returns):
    """
    Evaluate if portfolio following recommendations outperforms benchmark.
    """
    # Simulate portfolio following recommendations
    portfolio_returns = simulate_portfolio(recommendations)
    
    # Compare to benchmark (NIFTY50)
    benchmark_returns = get_nifty50_returns(same_period)
    
    metrics = {
        "total_return": portfolio_returns.sum(),
        "sharpe_ratio": calculate_sharpe(portfolio_returns),
        "max_drawdown": calculate_max_drawdown(portfolio_returns),
        "alpha": portfolio_returns.mean() - benchmark_returns.mean(),
        "win_rate": (portfolio_returns > 0).sum() / len(portfolio_returns)
    }
    
    return metrics
```

**Target Metrics:**
- Sharpe Ratio: >1.0
- Alpha vs NIFTY50: >3% annually
- Win Rate: >55%

---

#### 3. **Agent-Specific Metrics**

**Fundamental Agent:**
- Valuation accuracy (overvalued → price drops?)
- Earnings surprise correlation

**Technical Agent:**
- Entry/exit timing accuracy
- Trend prediction accuracy

**Sentiment Agent:**
- News impact prediction accuracy
- Sentiment vs price movement correlation

**Risk Agent:**
- Volatility prediction accuracy
- Drawdown estimation error

---

### B. Qualitative Metrics

#### 1. **Human Expert Evaluation**

Have financial analysts rate on 1-5 scale:

```
Evaluation Criteria:
1. Reasoning Quality: Is the logic sound?
2. Completeness: Are all important factors considered?
3. Actionability: Are recommendations clear and specific?
4. Risk Disclosure: Are risks adequately mentioned?
5. Regulatory Compliance: Any issues with disclaimers?

Average Score: Target >4.0/5.0
```

---

#### 2. **User Satisfaction Metrics**

```python
# Track in-app metrics
user_metrics = {
    "nps_score": 50,  # Net Promoter Score (target >40)
    "session_duration": 8.5,  # minutes (target >5)
    "return_rate": 0.65,  # 65% come back (target >60%)
    "recommendation_follow_rate": 0.45,  # 45% follow advice
    "thumbs_up_ratio": 0.75,  # 75% positive ratings
}
```

---

#### 3. **Hallucination Detection**

```python
def detect_hallucinations(agent_output, ground_truth_data):
    """
    Check if agent is making up facts.
    """
    hallucinations = []
    
    # Extract factual claims
    claims = extract_factual_claims(agent_output)
    
    for claim in claims:
        # Verify against ground truth
        if not verify_claim(claim, ground_truth_data):
            hallucinations.append(claim)
    
    hallucination_rate = len(hallucinations) / len(claims)
    
    return hallucination_rate  # Target <5%
```

---

## 3. Data Collection

### Training Data Sources

#### A. **Historical Stock Data**
```python
# Collect for each stock
historical_data = {
    "ticker": "RELIANCE.NS",
    "date_range": "2020-01-01 to 2026-08-26",
    "price_data": [...],
    "fundamental_data": [...],
    "news_data": [...],
    "events": [...]  # earnings, dividends, splits
}
```

#### B. **Expert Analyses**
- Broker research reports
- Financial analyst recommendations
- Past investment decisions with outcomes

#### C. **User Feedback**
```python
user_feedback = {
    "analysis_id": "12345",
    "ticker": "TCS.NS",
    "recommendation": "BUY",
    "user_rating": 5,  # 1-5 stars
    "user_comment": "Accurate analysis, bought at ₹3,500",
    "outcome": {
        "followed_recommendation": True,
        "entry_price": 3500,
        "exit_price": 3750,  # or current price
        "return": 7.1
    }
}
```

---

### Data Labeling

#### Option 1: Automated Labeling
```python
def auto_label_recommendation(stock_data, future_returns):
    """
    Automatically label what recommendation SHOULD have been.
    """
    if future_returns['1M'] > 10%:
        return "STRONG BUY"
    elif future_returns['1M'] > 5%:
        return "BUY"
    elif future_returns['1M'] > -5%:
        return "HOLD"
    elif future_returns['1M'] > -10%:
        return "SELL"
    else:
        return "STRONG SELL"
```

#### Option 2: Human Labeling
- Hire financial analysts to label 100-200 examples
- Use for validation set (gold standard)
- Compare model predictions to human expert labels

---

## 4. Implementation Steps

### Step 1: Prepare Fine-Tuning Dataset

```python
# scripts/prepare_training_data.py

import pandas as pd
import json
from financial_data_enhanced import FinancialDataProvider

def create_training_dataset(num_samples=1000):
    """Generate training dataset for fine-tuning."""
    
    training_data = []
    
    # Get list of stocks
    nifty50_stocks = get_nifty50_tickers()
    
    for i in range(num_samples):
        ticker = random.choice(nifty50_stocks)
        
        # Get historical data (use past data point)
        date = random_date_between("2022-01-01", "2025-12-31")
        stock_data = get_historical_stock_data(ticker, date)
        
        # Get future performance (for labeling)
        future_return_1m = get_future_return(ticker, date, days=30)
        
        # Create input
        input_text = format_input_for_agent(stock_data)
        
        # Create ideal output (either from expert or heuristic)
        output_text = create_ideal_analysis(
            stock_data, 
            future_return_1m,
            agent_type="fundamental"
        )
        
        training_data.append({
            "input": input_text,
            "output": output_text,
            "metadata": {
                "ticker": ticker,
                "date": date,
                "actual_return_1m": future_return_1m
            }
        })
    
    # Save as JSONL
    with open("training_data.jsonl", "w") as f:
        for item in training_data:
            f.write(json.dumps(item) + "\n")
    
    return training_data
```

---

### Step 2: Fine-Tune with Gemini API

```python
# scripts/fine_tune_agent.py

from google import genai

def fine_tune_fundamental_agent():
    """Fine-tune fundamental analysis agent."""
    
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    
    # Upload training data
    training_file = client.files.upload(
        path="training_data.jsonl"
    )
    
    # Create fine-tuning job
    tuning_job = client.tuning.create_job(
        model="gemini-2.0-flash-exp",
        training_data=training_file,
        hyperparameters={
            "epochs": 3,
            "batch_size": 32,
            "learning_rate": 0.001
        }
    )
    
    # Monitor progress
    while tuning_job.state != "COMPLETED":
        time.sleep(60)
        tuning_job = client.tuning.get_job(tuning_job.name)
        print(f"Progress: {tuning_job.progress}%")
    
    # Get fine-tuned model name
    fine_tuned_model = tuning_job.tuned_model
    print(f"Fine-tuned model: {fine_tuned_model}")
    
    return fine_tuned_model
```

---

### Step 3: Evaluation Pipeline

```python
# scripts/evaluate_agents.py

class AgentEvaluator:
    """Comprehensive evaluation framework for agents."""
    
    def __init__(self, agent, eval_dataset):
        self.agent = agent
        self.eval_dataset = eval_dataset
        self.results = []
    
    def run_evaluation(self):
        """Run full evaluation suite."""
        
        # 1. Accuracy metrics
        accuracy = self.evaluate_accuracy()
        
        # 2. Performance metrics
        performance = self.evaluate_performance()
        
        # 3. Quality metrics
        quality = self.evaluate_quality()
        
        # 4. Safety metrics
        safety = self.evaluate_safety()
        
        report = {
            "accuracy": accuracy,
            "performance": performance,
            "quality": quality,
            "safety": safety,
            "overall_score": self.calculate_overall_score()
        }
        
        return report
    
    def evaluate_accuracy(self):
        """Test recommendation accuracy."""
        correct = 0
        total = len(self.eval_dataset)
        
        for example in self.eval_dataset:
            prediction = self.agent.analyze(example['input'])
            
            # Compare to ground truth
            if self.predictions_match(
                prediction, 
                example['ground_truth']
            ):
                correct += 1
        
        return {
            "accuracy": correct / total,
            "total_examples": total
        }
    
    def evaluate_performance(self):
        """Test if following recommendations leads to good returns."""
        # Implement portfolio simulation
        # Compare to benchmark
        pass
    
    def evaluate_quality(self):
        """Evaluate output quality metrics."""
        return {
            "avg_response_length": self.calc_avg_length(),
            "format_consistency": self.check_format_consistency(),
            "citation_rate": self.check_citations(),
            "hallucination_rate": self.detect_hallucinations()
        }
    
    def evaluate_safety(self):
        """Check for unsafe recommendations."""
        return {
            "disclaimer_presence": self.check_disclaimers(),
            "extreme_predictions": self.count_extreme_predictions(),
            "regulatory_compliance": self.check_compliance()
        }
```

---

### Step 4: A/B Testing

```python
# app_multiagent.py

def get_agent_version():
    """Decide which agent version to use for this user."""
    
    user_id = get_user_id()
    
    # A/B test: 50% get fine-tuned, 50% get base model
    if user_id % 2 == 0:
        return FundamentalAnalysisAgent(model="fine-tuned-v1")
    else:
        return FundamentalAnalysisAgent(model="base")

# Track results
def track_recommendation(user_id, agent_version, recommendation, outcome):
    """Track which version performs better."""
    analytics.log({
        "user_id": user_id,
        "agent_version": agent_version,
        "recommendation": recommendation,
        "user_satisfaction": outcome.get("rating"),
        "recommendation_accuracy": outcome.get("accuracy")
    })
```

---

## 5. Continuous Improvement Loop

```
┌─────────────────────────────────────────┐
│  1. Collect User Feedback               │
│     - Ratings, comments                 │
│     - Actual outcomes                   │
└──────────────┬──────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────┐
│  2. Analyze Performance                 │
│     - Which recommendations worked?     │
│     - Where did agents fail?            │
└──────────────┬──────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────┐
│  3. Generate New Training Data          │
│     - Add successful examples           │
│     - Create adversarial examples       │
└──────────────┬──────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────┐
│  4. Retrain/Fine-Tune Models            │
│     - Monthly or quarterly              │
│     - Version control models            │
└──────────────┬──────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────┐
│  5. A/B Test New Version                │
│     - 10% of users get new version      │
│     - Monitor metrics carefully         │
└──────────────┬──────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────┐
│  6. Gradual Rollout                     │
│     - If better, roll out to all        │
│     - If worse, revert and iterate      │
└──────────────┬──────────────────────────┘
               │
               └──────── Loop Back ────────┘
```

---

## 6. Implementation Checklist

### Phase 1: Data Collection (Week 1-2)
- [ ] Collect 100 manual examples per agent
- [ ] Generate 500 synthetic examples per agent
- [ ] Create validation set (100 examples, human-labeled)
- [ ] Set up data versioning (DVC or similar)

### Phase 2: Baseline Evaluation (Week 3)
- [ ] Evaluate current zero-shot agents
- [ ] Establish baseline metrics
- [ ] Document failure cases

### Phase 3: Fine-Tuning (Week 4-5)
- [ ] Fine-tune fundamental agent (1000 examples)
- [ ] Fine-tune technical agent (1000 examples)
- [ ] Fine-tune other agents as needed
- [ ] Version control all models

### Phase 4: Evaluation (Week 6)
- [ ] Run evaluation pipeline
- [ ] Compare fine-tuned vs base
- [ ] Human expert review (10 analysts, 20 examples each)
- [ ] Fix critical issues

### Phase 5: Deployment (Week 7-8)
- [ ] A/B test framework setup
- [ ] Deploy to 10% of users
- [ ] Monitor metrics daily
- [ ] Gradual rollout if successful

### Phase 6: Continuous Improvement (Ongoing)
- [ ] Monthly retraining with new data
- [ ] Quarterly full evaluation
- [ ] User feedback integration
- [ ] Model versioning and rollback capability

---

## 7. Tools and Frameworks

### Recommended Stack

```bash
# Fine-tuning
pip install transformers  # Hugging Face
pip install peft  # LoRA
pip install bitsandbytes  # Quantization

# Evaluation
pip install evaluate  # Metrics
pip install rouge-score  # Text quality
pip install bert-score  # Semantic similarity

# Data & Tracking
pip install datasets  # Data management
pip install wandb  # Experiment tracking
pip install mlflow  # Model versioning

# RAG (if implementing)
pip install chromadb  # Vector database
pip install sentence-transformers  # Embeddings
pip install langchain  # RAG framework
```

---

## 8. Cost Estimation

### Fine-Tuning Costs (Google Gemini)

```
Training Data: 1000 examples × 7 agents = 7000 examples
Cost per 1000 examples: ~$20-50
Total Fine-Tuning Cost: $140-350 one-time

Monthly Inference (10K users, 50K analyses):
Base Model: ~$500/month
Fine-Tuned Model: ~$300/month (smaller model)
Savings: $200/month

ROI: Break even in 2 months
```

---

## Next Steps

1. **Start Small**: Fine-tune one agent (Fundamental) first
2. **Measure Everything**: Set up tracking before fine-tuning
3. **Iterate**: Use data to continuously improve
4. **Scale**: Once process works, apply to all agents

**Ready to implement?** Start with `scripts/prepare_training_data.py`!
