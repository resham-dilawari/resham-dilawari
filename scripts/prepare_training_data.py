"""
Prepare Training Data for Fine-Tuning
Generates high-quality training examples for each agent
"""
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
import yfinance as yf


class TrainingDataGenerator:
    """Generate training data for fine-tuning agents."""
    
    def __init__(self):
        # NSE/BSE stock universe
        self.stock_universe = [
            "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
            "HINDUNILVR.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "KOTAKBANK.NS",
            "LT.NS", "AXISBANK.NS", "ASIANPAINT.NS", "MARUTI.NS", "TITAN.NS",
            "SUNPHARMA.NS", "ULTRACEMCO.NS", "NESTLEIND.NS", "WIPRO.NS", "ONGC.NS"
        ]
        
        self.training_examples = []
    
    def generate_fundamental_example(self, ticker: str) -> Dict[str, str]:
        """Generate a fundamental analysis training example."""
        
        try:
            # Fetch real data
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Extract metrics
            pe_ratio = info.get('trailingPE', random.uniform(15, 35))
            roe = info.get('returnOnEquity', random.uniform(0.08, 0.25))
            debt_to_equity = info.get('debtToEquity', random.uniform(0.2, 1.5))
            revenue_growth = info.get('revenueGrowth', random.uniform(-0.05, 0.30))
            profit_margin = info.get('profitMargins', random.uniform(0.05, 0.25))
            current_price = info.get('currentPrice', random.uniform(100, 5000))
            
            # Create input
            input_text = f"""Analyze {ticker} from a fundamental perspective.

Business Summary: {info.get('longBusinessSummary', 'Leading company in its sector')}
Current Price: ₹{current_price:.2f}
P/E Ratio: {pe_ratio:.2f}
ROE: {roe*100:.2f}%
Debt to Equity: {debt_to_equity:.2f}
Profit Margin: {profit_margin*100:.2f}%
Revenue Growth: {revenue_growth*100:.2f}%

Provide comprehensive fundamental analysis with rating."""
            
            # Generate ideal output
            # Determine rating based on metrics
            score = 0
            if roe > 0.15: score += 2
            elif roe > 0.12: score += 1
            
            if pe_ratio < 20: score += 2
            elif pe_ratio < 25: score += 1
            elif pe_ratio > 30: score -= 1
            
            if debt_to_equity < 0.5: score += 1
            elif debt_to_equity > 1.0: score -= 1
            
            if revenue_growth > 0.15: score += 2
            elif revenue_growth > 0.10: score += 1
            elif revenue_growth < 0: score -= 2
            
            if score >= 5:
                rating = "STRONG BUY"
                confidence = "HIGH"
            elif score >= 3:
                rating = "BUY"
                confidence = "MEDIUM"
            elif score >= 0:
                rating = "HOLD"
                confidence = "MEDIUM"
            else:
                rating = "SELL"
                confidence = "MEDIUM"
            
            output_text = f"""**Executive Summary**
{ticker} shows {"strong" if score > 3 else "moderate" if score > 0 else "weak"} fundamentals with ROE of {roe*100:.1f}% and revenue growth of {revenue_growth*100:.1f}%. {"Conservative" if debt_to_equity < 0.7 else "Elevated"} debt management with D/E of {debt_to_equity:.2f}. P/E of {pe_ratio:.1f} {"indicates fair valuation" if 18 < pe_ratio < 25 else "suggests premium valuation" if pe_ratio >= 25 else "indicates attractive valuation"}.

**Detailed Analysis**

1. **Financial Health ({min(10, max(1, score+5))}/10)**
   - ROE of {roe*100:.1f}%: {"Excellent" if roe > 0.20 else "Good" if roe > 0.15 else "Average" if roe > 0.12 else "Below average"} capital efficiency
   - Debt/Equity {debt_to_equity:.2f}: {"Conservative" if debt_to_equity < 0.5 else "Moderate" if debt_to_equity < 1.0 else "High"} leverage
   - Profit margin {profit_margin*100:.1f}%: {"Strong" if profit_margin > 0.15 else "Healthy" if profit_margin > 0.10 else "Adequate"} profitability

2. **Growth Prospects ({min(10, max(1, int(revenue_growth*50)))}/10)**
   - Revenue growth {revenue_growth*100:.1f}%: {"Strong momentum" if revenue_growth > 0.15 else "Moderate growth" if revenue_growth > 0.08 else "Slow growth" if revenue_growth > 0 else "Decline"}
   - {"Positive" if revenue_growth > 0.10 else "Stable" if revenue_growth > 0 else "Concerning"} trajectory

3. **Valuation ({min(10, max(1, int((30-pe_ratio)/2)))}/10)**
   - P/E {pe_ratio:.1f}: {"Premium to sector" if pe_ratio > 25 else "Inline with sector" if pe_ratio > 18 else "Discount to sector"}
   - {"Growth premium justified" if revenue_growth > 0.15 and pe_ratio > 25 else "Fair valuation" if 18 < pe_ratio < 25 else "Attractive entry point"}

**Key Insights**
- {"Strong" if roe > 0.15 else "Stable"} fundamental foundation
- {"Premium" if pe_ratio > 25 else "Fair" if pe_ratio > 18 else "Attractive"} valuation
- {"High" if debt_to_equity > 1.0 else "Low" if debt_to_equity < 0.5 else "Moderate"} financial risk

**Rating: {rating}**
**Target Price: ₹{current_price * (1.1 if score > 3 else 1.05 if score > 0 else 0.95):.0f}**
**Confidence: {confidence}**
**Timeframe: 6-12 months**

**Risks & Limitations**
- Valuation risk if market multiples compress
- Sector-specific regulatory or competitive risks
- Macro economic factors (interest rates, inflation)
- Company-specific execution risks"""
            
            return {
                "input": input_text,
                "output": output_text,
                "metadata": {
                    "ticker": ticker,
                    "agent": "fundamental",
                    "rating": rating,
                    "date": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            print(f"Error generating example for {ticker}: {e}")
            return None
    
    def generate_technical_example(self, ticker: str) -> Dict[str, str]:
        """Generate a technical analysis training example."""
        
        # Generate mock technical data
        current_price = random.uniform(100, 5000)
        ma_50 = current_price * random.uniform(0.95, 1.05)
        ma_200 = current_price * random.uniform(0.90, 1.10)
        rsi = random.uniform(30, 70)
        week_52_high = current_price * random.uniform(1.0, 1.3)
        week_52_low = current_price * random.uniform(0.7, 1.0)
        
        input_text = f"""Perform technical analysis on {ticker}.

Current Price: ₹{current_price:.2f}
50-Day MA: ₹{ma_50:.2f}
200-Day MA: ₹{ma_200:.2f}
RSI (14): {rsi:.1f}
52-Week High: ₹{week_52_high:.2f}
52-Week Low: ₹{week_52_low:.2f}

Provide technical analysis with entry/exit points."""
        
        # Determine trend and rating
        if current_price > ma_50 > ma_200 and rsi < 70:
            trend = "Uptrend"
            rating = "BUY"
        elif current_price < ma_50 < ma_200 and rsi > 30:
            trend = "Downtrend"
            rating = "SELL"
        else:
            trend = "Sideways"
            rating = "HOLD"
        
        output_text = f"""**Executive Summary**
{ticker} in {trend} with price {"above" if current_price > ma_50 else "below"} key moving averages. RSI at {rsi:.0f} indicates {"overbought" if rsi > 70 else "oversold" if rsi < 30 else "neutral"} conditions.

**Technical Analysis**

1. **Trend Analysis**
   - Primary Trend: {trend}
   - Price vs 50-MA: {"Bullish" if current_price > ma_50 else "Bearish"} (₹{abs(current_price - ma_50):.0f} {"above" if current_price > ma_50 else "below"})
   - Price vs 200-MA: {"Bullish" if current_price > ma_200 else "Bearish"} (₹{abs(current_price - ma_200):.0f} {"above" if current_price > ma_200 else "below"})

2. **Momentum Indicators**
   - RSI: {rsi:.1f} ({"Overbought" if rsi > 70 else "Oversold" if rsi < 30 else "Neutral zone"})
   - {"Strong" if abs(rsi - 50) > 20 else "Moderate"} momentum

3. **Support & Resistance**
   - Resistance: ₹{week_52_high:.0f} (52W high)
   - Support: ₹{max(ma_200, week_52_low):.0f}
   - Current position: {((current_price - week_52_low)/(week_52_high - week_52_low)*100):.0f}% of 52W range

**Key Technical Insights**
- {trend} pattern confirmed
- {"Golden cross" if ma_50 > ma_200 else "Death cross" if ma_50 < ma_200 else "MAs converging"}
- {"Overbought" if rsi > 70 else "Oversold" if rsi < 30 else "Neutral"} momentum

**Rating: {rating}**
{"**Entry Point: ₹" + f"{current_price * 0.97:.0f}**" if rating == "BUY" else ""}
{"**Stop Loss: ₹" + f"{current_price * 0.95:.0f}**" if rating == "BUY" else ""}
**Confidence: {"HIGH" if abs(rsi - 50) > 20 else "MEDIUM"}**
**Timeframe: 1-4 weeks**"""
        
        return {
            "input": input_text,
            "output": output_text,
            "metadata": {
                "ticker": ticker,
                "agent": "technical",
                "rating": rating,
                "date": datetime.now().isoformat()
            }
        }
    
    def generate_risk_example(self, ticker: str) -> Dict[str, str]:
        """Generate a risk assessment training example."""
        
        beta = random.uniform(0.6, 1.8)
        volatility = random.uniform(15, 45)
        max_drawdown = -random.uniform(15, 35)
        sharpe_ratio = random.uniform(0.5, 2.5)
        
        input_text = f"""Assess risk for {ticker}.

Beta: {beta:.2f}
Historical Volatility: {volatility:.1f}%
Maximum Drawdown: {max_drawdown:.1f}%
Sharpe Ratio: {sharpe_ratio:.2f}

Provide risk assessment with suitability."""
        
        # Determine risk level
        if beta > 1.3 or volatility > 30:
            risk_level = "HIGH RISK"
        elif beta > 1.0 or volatility > 22:
            risk_level = "MODERATE RISK"
        else:
            risk_level = "LOW RISK"
        
        output_text = f"""**Risk Assessment: {risk_level}**

**Risk Metrics Analysis**

1. **Systematic Risk**
   - Beta {beta:.2f}: {beta*100-100:+.0f}% {"more" if beta > 1 else "less"} volatile than market
   - {"High" if beta > 1.3 else "Moderate" if beta > 1.0 else "Low"} market correlation

2. **Total Volatility**
   - Annual volatility {volatility:.1f}%: {"Well above" if volatility > 30 else "Above" if volatility > 22 else "Below"} market average (18-22%)
   - Maximum drawdown {max_drawdown:.1f}%: {"Significant" if max_drawdown < -25 else "Moderate" if max_drawdown < -20 else "Limited"} downside

3. **Risk-Adjusted Returns**
   - Sharpe ratio {sharpe_ratio:.2f}: {"Excellent" if sharpe_ratio > 1.5 else "Good" if sharpe_ratio > 1.0 else "Poor" if sharpe_ratio < 0.7 else "Fair"} risk-adjusted performance
   - {"High quality" if sharpe_ratio > 1.5 else "Acceptable" if sharpe_ratio > 0.8 else "Low quality"} returns

**Investor Suitability**
- {"❌" if risk_level == "HIGH RISK" else "⚠️" if risk_level == "MODERATE RISK" else "✅"} Conservative investors
- {"⚠️" if risk_level == "HIGH RISK" else "✅"} Moderate risk investors
- ✅ Aggressive investors {"with 3+ year horizon" if risk_level == "HIGH RISK" else ""}

**Risk Mitigation Strategies**
- Limit allocation to {10 if risk_level == "HIGH RISK" else 15 if risk_level == "MODERATE RISK" else 25}% of portfolio
- Pair with low-beta defensive stocks
- {"Use stop-loss at -15%" if risk_level == "HIGH RISK" else "Monitor quarterly"}
- {"Dollar-cost average" if risk_level == "HIGH RISK" else "Consider lump-sum"}

**Confidence: HIGH**"""
        
        return {
            "input": input_text,
            "output": output_text,
            "metadata": {
                "ticker": ticker,
                "agent": "risk",
                "risk_level": risk_level,
                "date": datetime.now().isoformat()
            }
        }
    
    def generate_training_dataset(self, 
                                  num_examples_per_agent: int = 100,
                                  agents: List[str] = None) -> List[Dict]:
        """Generate complete training dataset."""
        
        if agents is None:
            agents = ["fundamental", "technical", "risk"]
        
        print(f"🎓 Generating training data for {len(agents)} agents...")
        print(f"   Target: {num_examples_per_agent} examples per agent")
        
        all_examples = []
        
        for agent in agents:
            print(f"\n📊 Generating {agent} examples...")
            agent_examples = []
            
            for i in range(num_examples_per_agent):
                ticker = random.choice(self.stock_universe)
                
                if agent == "fundamental":
                    example = self.generate_fundamental_example(ticker)
                elif agent == "technical":
                    example = self.generate_technical_example(ticker)
                elif agent == "risk":
                    example = self.generate_risk_example(ticker)
                else:
                    continue
                
                if example:
                    agent_examples.append(example)
                
                if (i + 1) % 20 == 0:
                    print(f"   Progress: {i+1}/{num_examples_per_agent}")
            
            print(f"   ✅ Generated {len(agent_examples)} {agent} examples")
            all_examples.extend(agent_examples)
        
        print(f"\n✅ Total examples generated: {len(all_examples)}")
        return all_examples
    
    def save_training_data(self, 
                          examples: List[Dict],
                          filename: str = "training_data.jsonl"):
        """Save training data in JSONL format for fine-tuning."""
        
        print(f"\n💾 Saving to {filename}...")
        
        with open(filename, 'w', encoding='utf-8') as f:
            for example in examples:
                # Keep only input/output for training
                training_example = {
                    "input": example["input"],
                    "output": example["output"]
                }
                f.write(json.dumps(training_example, ensure_ascii=False) + '\n')
        
        print(f"✅ Saved {len(examples)} examples to {filename}")
        
        # Also save with metadata for analysis
        metadata_file = filename.replace('.jsonl', '_with_metadata.json')
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(examples, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved metadata version to {metadata_file}")


def main():
    """Main function to generate training data."""
    
    print("=" * 60)
    print("TRAINING DATA GENERATION")
    print("=" * 60)
    
    generator = TrainingDataGenerator()
    
    # Generate training data
    examples = generator.generate_training_dataset(
        num_examples_per_agent=20,  # Start small for testing
        agents=["fundamental", "technical", "risk"]
    )
    
    # Save
    generator.save_training_data(examples, "training_data.jsonl")
    
    # Show samples
    print("\n📝 Sample Training Example:")
    print("=" * 60)
    sample = random.choice(examples)
    print(f"Agent: {sample['metadata']['agent']}")
    print(f"\nINPUT:\n{sample['input'][:300]}...")
    print(f"\nOUTPUT:\n{sample['output'][:300]}...")
    print("=" * 60)
    
    print(f"\n✅ Training data ready! Next steps:")
    print(f"   1. Review training_data.jsonl")
    print(f"   2. Upload to Gemini for fine-tuning")
    print(f"   3. Run fine-tuning job")
    print(f"   4. Evaluate fine-tuned model")


if __name__ == "__main__":
    main()
