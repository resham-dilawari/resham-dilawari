# 📋 Product Naming Guide

## Naming Clarity: Stock Advisor vs Portfolio Advisor

### ✅ Current Product: **Stock Advisor**

**Why "Stock Advisor" not "Portfolio Advisor"?**

Our product currently focuses **exclusively on equities/stocks** listed on Indian exchanges (NSE/BSE). We do NOT cover:
- ❌ Mutual Funds (MFs)
- ❌ Bonds / Fixed Income
- ❌ Real Estate / REITs
- ❌ Gold / Commodities
- ❌ Crypto assets
- ❌ International stocks

**What we DO cover:**
- ✅ Individual stocks (NSE/BSE)
- ✅ Stock risk analytics
- ✅ Multi-stock allocation optimization
- ✅ Stock news sentiment
- ✅ Stock technical analysis
- ✅ Stock fundamental analysis

---

## When to Use Each Term

### Use "Stock Advisor" when:
- Product focuses ONLY on equities/stocks
- Single asset class coverage
- Stock-specific analysis (P/E, EPS, stock charts, etc.)
- Our current implementation ✅

### Use "Portfolio Advisor" when:
- Product covers MULTIPLE asset classes
- Includes: Stocks + MFs + Bonds + Real Estate + etc.
- True portfolio diversification across asset types
- Asset allocation between different asset classes
- Future enhancement 🚀

---

## Current Product Architecture

```
AI Stock Advisor (Current)
├── Stocks/Equities Only
│   ├── NSE listed companies (.NS)
│   ├── BSE listed companies (.BO)
│   └── Indian equity markets
│
├── Analysis Types
│   ├── Individual stock analysis
│   ├── Multi-stock holdings analysis
│   ├── Risk analytics (stock-level)
│   └── Tax optimization (STCG/LTCG)
│
└── NOT Covered
    ├── Mutual Funds
    ├── Bonds
    ├── Real Estate
    └── Other assets
```

---

## Unified Platform: Two Products

### Product 1: **Stock Advisor** (WealthTech)
- **Target**: Retail investors
- **Focus**: Equities/stocks only
- **Agents**: 8 specialized for stock analysis
- **Output**: BUY/HOLD/SELL stock recommendations

### Product 2: **Merchant Underwriting** (B2B Fintech)
- **Target**: Risk analysts (internal users)
- **Focus**: Business entity screening
- **Agents**: 5 specialized for KYC/KYB
- **Output**: Risk assessment brief

---

## Future Expansion Path

### Phase 1: Stock Advisor (Current) ✅
- Equities only
- NSE/BSE coverage
- Stock-focused agents

### Phase 2: Portfolio Advisor (Future)
- Add Mutual Fund analysis agent
- Add Bond/Fixed Income agent
- Add Real Estate/REIT agent
- Add Asset Allocation agent (cross-asset)
- Rename to "Portfolio Advisor"

---

## User-Facing Communication

### ✅ Correct Messaging:
> "AI Stock Advisor - Get personalized stock recommendations, risk analysis, and market insights for Indian equities (NSE/BSE)."

> "Focused on stocks/equities only. For multi-asset portfolio management, see our Portfolio Advisor (coming soon)."

### ❌ Avoid:
> "Portfolio Advisor" - misleading if only stocks

> "Complete portfolio management" - implies multi-asset

> "Asset allocation" without clarifying stock-only

---

## Technical Implementation

### File Naming:
- `app_multiagent.py` → Stock Advisor UI
- `app_underwriting.py` → Merchant Underwriting UI
- `app_unified.py` → Product selector dashboard

### Display Names:
- **Dashboard**: "AI Stock Advisor"
- **Page Title**: "Multi-Agent Stock Advisor"
- **Button**: "Launch Stock Advisor"

### Code References:
```python
st.title("📈 Multi-Agent Stock Advisor")
st.markdown("AI-Powered Stock Research & Analysis for Indian Equities")
```

---

## Interview Talking Points

**When asked: "Why Stock Advisor not Portfolio Advisor?"**

> "Great question! I specifically chose 'Stock Advisor' because the product currently focuses exclusively on equities listed on NSE/BSE. It provides deep stock-level analysis using 8 specialized agents.
>
> The term 'Portfolio Advisor' would be misleading since we don't cover mutual funds, bonds, real estate, or other asset classes. If we were to expand to multi-asset coverage, we'd add agents for those asset classes and rebrand to 'Portfolio Advisor'.
>
> This naming precision is important for:
> 1. Setting correct user expectations
> 2. Clear product positioning
> 3. Future expansion path clarity
> 4. Honest marketing - we don't overpromise"

---

## Competitive Positioning

### vs Generic "Portfolio" Tools:
- ❌ They claim "portfolio" but only do stocks
- ✅ We're honest: "Stock Advisor" = stocks only
- ✅ Clear positioning builds trust

### vs Multi-Asset Platforms:
- ❌ They're too broad, analysis is shallow
- ✅ We go deep on stocks with 8 specialized agents
- ✅ Better to be excellent at one thing than mediocre at many

---

## Product Evolution Roadmap

```
v1.0: Stock Advisor (Current)
├── Stocks only (NSE/BSE)
├── 8 specialized agents
└── 3 personas

v2.0: Enhanced Stock Advisor (Next 3-6 months)
├── Options trading analysis
├── Sector rotation strategies
├── International stocks (US markets)
└── Advanced charting

v3.0: Portfolio Advisor (6-12 months)
├── Add Mutual Fund agent
├── Add Bond/Fixed Income agent
├── Add Real Estate/REIT agent
├── Cross-asset allocation optimizer
└── Rebrand to "Portfolio Advisor"
```

---

## Summary

| Aspect | Current | Future |
|--------|---------|--------|
| **Name** | Stock Advisor | Portfolio Advisor |
| **Coverage** | Stocks only | Multi-asset |
| **Assets** | Equities (NSE/BSE) | Stocks + MFs + Bonds + RE |
| **Agents** | 8 (stock-focused) | 12+ (multi-asset) |
| **Status** | ✅ Implemented | 🚀 Roadmap |

**Bottom Line**: We're a **Stock Advisor** today, with a clear path to becoming a **Portfolio Advisor** tomorrow.

---

**Accuracy in naming = Trust with users** ✅
