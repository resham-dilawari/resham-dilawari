"""
Index Sample Data into RAG System
Populates the vector database with demo financial documents
"""
from setup_rag import RAGSystem
from datetime import datetime, timedelta

def index_sample_data():
    """Index comprehensive sample financial data."""
    
    print("🚀 Starting sample data indexing...")
    print("=" * 60)
    
    # Initialize RAG system
    rag = RAGSystem(persist_directory="./chroma_db")
    
    # Sample 1: RELIANCE Stock Analysis
    print("\n📊 Indexing RELIANCE.NS analysis...")
    rag.index_stock_analysis(
        ticker="RELIANCE.NS",
        analysis="""
**RELIANCE Industries - Comprehensive Analysis (December 2025)**

**Executive Summary:**
RELIANCE shows robust fundamentals with strong diversification across energy, retail, and digital sectors. 
Current valuation at P/E of 24.5x appears reasonable given growth trajectory.

**Key Metrics:**
- Market Cap: ₹17.5 trillion
- P/E Ratio: 24.5x (slightly above 5-year average of 22x)
- ROE: 12.8% (industry average: 10-12%)
- Debt/Equity: 0.45 (conservative leverage)
- Revenue Growth (YoY): 18%
- Net Profit Margin: 9.2%

**Business Segments:**
1. **O2C (Oil-to-Chemicals)**: 60% of revenue, stable cash flows
2. **Retail**: 15% of revenue, fastest growing at 25% YoY
3. **Digital (Jio)**: 10% of revenue, 450M+ subscribers
4. **New Energy**: Emerging segment, significant capex commitment

**Rating: HOLD with positive bias**
**Target Price: ₹2,800 (upside potential: 12%)**
**Confidence Level: HIGH**
**Risk Level: MEDIUM**

Key risks: Crude oil volatility, regulatory changes in telecom, execution risk in new energy ventures.
""",
        agent="fundamental_agent",
        metadata={"date": (datetime.now() - timedelta(days=30)).isoformat(), "confidence": "HIGH"}
    )
    
    # Sample 2: TCS Stock Analysis
    print("📊 Indexing TCS.NS analysis...")
    rag.index_stock_analysis(
        ticker="TCS.NS",
        analysis="""
**TCS - IT Sector Leader Analysis (November 2025)**

**Executive Summary:**
TCS maintains its position as India's largest IT services company with consistent performance.
Defensive characteristics make it suitable for risk-averse portfolios.

**Key Metrics:**
- Market Cap: ₹13.2 trillion
- P/E Ratio: 28.5x (premium to sector average of 25x justified by quality)
- ROE: 45% (exceptional capital efficiency)
- Debt/Equity: 0.0 (debt-free)
- Revenue Growth: 12% (steady)
- Operating Margin: 25% (industry-leading)

**Strengths:**
- Diversified client base across geographies
- Strong digital transformation portfolio
- Consistent dividend payer (2.5% yield)
- Recession-resistant business model

**Rating: BUY for long-term**
**Target Price: ₹4,200 (upside: 8%)**
**Confidence: HIGH**
**Risk Level: LOW**

Concerns: Slower growth compared to mid-tier IT companies, exposure to US tech slowdown.
""",
        agent="fundamental_agent",
        metadata={"date": (datetime.now() - timedelta(days=20)).isoformat()}
    )
    
    # Sample 3: HDFC Bank Analysis
    print("📊 Indexing HDFCBANK.NS analysis...")
    rag.index_stock_analysis(
        ticker="HDFCBANK.NS",
        analysis="""
**HDFC Bank - Banking Sector Analysis (December 2025)**

**Post-merger Integration Analysis**

**Key Metrics:**
- P/E Ratio: 19.5x
- P/B Ratio: 2.8x
- ROE: 17% (adjusting post-merger)
- CASA Ratio: 42%
- NPA: 1.1% (best in class)
- Loan Growth: 15% YoY

**Post-Merger Dynamics:**
HDFC Bank merger with HDFC Ltd completed. Initial integration challenges being managed well.
Scale benefits emerging - now India's largest bank by market cap.

**Rating: ACCUMULATE**
**Target: ₹1,850**
**Risk: MEDIUM**

Near-term headwinds from integration, but long-term story intact.
""",
        agent="fundamental_agent",
        metadata={"date": (datetime.now() - timedelta(days=15)).isoformat()}
    )
    
    # Sample 4: Regulatory Document - Tax Rules
    print("📄 Indexing tax regulations...")
    rag.index_document(
        doc_type="regulatory_docs",
        text="""
**Indian Capital Gains Tax - 2026 Update**

**Equity Investments:**

**Long-Term Capital Gains (LTCG):**
- Holding Period: > 12 months
- Tax Rate: 12.5% on gains exceeding ₹1.25 lakh per year
- Exemption: First ₹1.25 lakh is tax-free
- Listed equity shares and equity mutual funds qualify

**Short-Term Capital Gains (STCG):**
- Holding Period: ≤ 12 months  
- Tax Rate: 20% (flat rate)
- No exemption limit
- Applied to gains from equity shares and equity MFs

**Tax Loss Harvesting Strategy:**
- STCG losses can offset STCG/LTCG gains
- LTCG losses can only offset LTCG gains
- Losses can be carried forward for 8 years
- Booking losses before March 31 (FY end) maximizes benefit

**Section 80C Deductions:**
- ELSS (Equity Linked Savings Scheme) qualifies
- Maximum deduction: ₹1.5 lakh per year
- Lock-in period: 3 years
- Tax savings: Up to ₹46,800 for highest tax bracket (30%)

**Important:** These rules are subject to change in Union Budget. Consult tax advisor before major decisions.
""",
        metadata={
            "source": "Income Tax Act 2026",
            "category": "taxation",
            "last_updated": datetime.now().isoformat()
        }
    )
    
    # Sample 5: Market Research - IT Sector
    print("📄 Indexing IT sector research...")
    rag.index_document(
        doc_type="market_research",
        text="""
**Indian IT Sector Outlook - 2026**

**Sector Overview:**
Indian IT services sector expected to reach $250B in revenue by FY26, growing at 12-15% CAGR.

**Key Trends:**
1. **Digital Transformation:** 65% of revenue now from digital services (cloud, AI/ML, automation)
2. **Deal Pipeline:** Strong deal momentum continues, TCV (Total Contract Value) up 25% YoY
3. **Margin Pressure:** Wage inflation (8-10%) and travel costs resuming post-pandemic
4. **Geographical Mix:** USA 60%, Europe 25%, India 10%, RoW 5%

**Top Companies Performance:**
- **TCS:** Maintaining leadership, 12% growth, 25% margins
- **Infosys:** Aggressive digital push, 15% growth, 23% margins  
- **HCL Tech:** Product focus, 13% growth, 19% margins
- **Wipro:** Turnaround underway, 10% growth, 17% margins

**Sector Rating: OVERWEIGHT**

**Valuations:**
Average P/E: 25x (vs 5-year average of 22x)
Slight premium justified by:
- Strong deal wins
- Digital revenue mix
- Stable USD/INR around 83

**Risk Factors:**
- US recession fears
- Client budget cuts in BFSI sector
- Visa restrictions (H1-B uncertainty)
- Competition from GCCs (Global Capability Centers)

**Investment Strategy:**
- Prefer large-caps (TCS, Infosys) for stability
- Mid-caps (Persistent, Coforge) for growth
- Avoid companies with high BFSI concentration (>40%)

**Sector PE:** 25x | **PB:** 5.2x | **Dividend Yield:** 2.1%
""",
        metadata={
            "source": "Market Research Report Q4 2025",
            "sector": "Information Technology",
            "analyst": "Research Team"
        }
    )
    
    # Sample 6: Risk Management Framework
    print("📄 Indexing risk framework...")
    rag.index_document(
        doc_type="regulatory_docs",
        text="""
**Portfolio Risk Management Framework for Retail Investors**

**Risk Classification:**

**LOW RISK (Conservative):**
- Volatility: < 15% annually
- Beta: 0.5 - 0.8
- Recommended allocation: 70-80% of portfolio
- Examples: Large-cap blue chips, debt funds, gold
- Suitable for: Retirees, capital preservation goals

**MEDIUM RISK (Moderate):**
- Volatility: 15-25% annually
- Beta: 0.8 - 1.2
- Recommended allocation: 50-60% of portfolio
- Examples: Diversified large & mid caps, balanced funds
- Suitable for: 5-10 year goals, moderate risk appetite

**HIGH RISK (Aggressive):**
- Volatility: > 25% annually
- Beta: > 1.2
- Recommended allocation: 20-30% of portfolio  
- Examples: Small-caps, sector funds, leveraged products
- Suitable for: Young investors, long horizon (10+ years)

**Diversification Guidelines:**
- Minimum 8 stocks, maximum 15 stocks for retail portfolio
- No single stock > 20% of portfolio
- No single sector > 30% of portfolio
- Geographic diversification: Consider international exposure (10-15%)

**Risk Metrics to Monitor:**
- **Sharpe Ratio:** > 1 is good, > 2 is excellent
- **Maximum Drawdown:** Should be within tolerance (typically 20-30%)
- **Beta:** Indicates systematic risk relative to market
- **Standard Deviation:** Measures volatility

**Rebalancing Triggers:**
- Annual rebalancing (minimum)
- When any asset class deviates > 10% from target allocation
- After major market movements (+/- 15%)
- When personal risk profile changes

**Stop-Loss Strategy:**
- Individual stocks: 15-20% trailing stop loss
- Portfolio level: 25% from peak (review positions)
- Review thesis if stock falls 30% - fundamental issue?

**Position Sizing:**
- High conviction: 10-15% of portfolio
- Medium conviction: 5-10%
- Low conviction / speculative: < 5%
- New positions: Start with half intended size, average if thesis plays out
""",
        metadata={
            "source": "Risk Management Guidelines 2026",
            "category": "risk_framework"
        }
    )
    
    # Sample 7: Recent INFY analysis
    print("📊 Indexing INFY.NS analysis...")
    rag.index_stock_analysis(
        ticker="INFY.NS",
        analysis="""
**Infosys - Growth vs Value Debate (December 2025)**

**Current Status:**
Infosys trading at P/E of 26x, near historical highs. Growth acceleration impressive but sustainability questioned.

**Key Metrics:**
- Revenue Growth: 15% YoY (beating TCS's 12%)
- Operating Margin: 21.5% (target 22-24%)
- Large Deals: $3.2B TCV in Q3 (strong pipeline)
- Attrition: 18% (down from 28% peak, but still elevated)

**Bull Case:**
- Digital revenue 67% of total (highest in sector)
- Aggressive deal wins in BFSI and retail
- Strong leadership under CEO Salil Parekh
- Cost optimization initiatives showing results

**Bear Case:**
- Valuation premium (26x vs TCS 28x, but TCS has better quality)
- Margin pressure from wage hikes and travel costs
- Execution risk on mega deals
- US client budget cuts looming

**Rating: NEUTRAL**  
**Target: ₹1,650 (Limited upside from current ₹1,600)**
**Recommendation:** HOLD existing positions, not a fresh BUY at current levels

**Better Entry:** Wait for correction to ₹1,450-1,500 range (24x PE)
""",
        agent="fundamental_agent",
        metadata={"date": datetime.now().isoformat()}
    )
    
    # Print statistics
    print("\n" + "=" * 60)
    print("✅ Sample Data Indexing Complete!")
    print("=" * 60)
    
    stats = rag.stats()
    print(f"\n📊 Database Statistics:")
    for collection, count in stats.items():
        print(f"   • {collection}: {count} documents")
    
    print(f"\n💾 Database Location: ./chroma_db")
    print(f"✨ RAG system ready for use!")
    print("\n🔍 Test Retrieval:")
    print("   - Query: 'RELIANCE stock analysis'")
    
    # Test retrieval
    results = rag.retrieve("RELIANCE stock fundamental analysis", n_results=2)
    print(f"   - Found: {len(results)} relevant documents")
    if results:
        print(f"   - Top Result: {results[0]['metadata']['source']} (Score: {results[0]['relevance_score']:.2f})")
    
    print("\n" + "=" * 60)
    return rag


if __name__ == "__main__":
    rag = index_sample_data()
