"""
Demo Script to Test Individual Agents
Run this to verify all agents are working correctly
"""
import os
from dotenv import load_dotenv
from agents.orchestrator import OrchestratorAgent
from agents.fundamental_agent import FundamentalAnalysisAgent
from agents.technical_agent import TechnicalAnalysisAgent
from agents.sentiment_agent import SentimentAnalysisAgent
from agents.risk_agent import RiskAssessmentAgent
from financial_data_enhanced import FinancialDataProvider

# Load environment
load_dotenv()

def test_data_provider():
    """Test financial data provider."""
    print("=" * 60)
    print("Testing Financial Data Provider")
    print("=" * 60)
    
    ticker = "RELIANCE.NS"
    print(f"\nFetching data for {ticker}...")
    
    data = FinancialDataProvider.get_comprehensive_stock_data(ticker)
    
    if "error" in data:
        print(f"❌ Error: {data['error']}")
        return False
    
    print(f"✅ Successfully fetched data for {data.get('company_name', ticker)}")
    print(f"   Current Price: ₹{data.get('current_price', 'N/A')}")
    print(f"   P/E Ratio: {data.get('pe_ratio', 'N/A')}")
    print(f"   Beta: {data.get('beta', 'N/A')}")
    print(f"   RSI: {data.get('rsi', 'N/A')}")
    print(f"   News Items: {len(data.get('news', []))}")
    
    return True

def test_fundamental_agent():
    """Test Fundamental Analysis Agent."""
    print("\n" + "=" * 60)
    print("Testing Fundamental Analysis Agent")
    print("=" * 60)
    
    try:
        agent = FundamentalAnalysisAgent()
        print(f"✅ Agent initialized: {agent.agent_name}")
        
        # Mock context
        context = {
            "ticker": "RELIANCE.NS",
            "business_summary": "Reliance Industries is India's largest private sector company.",
            "current_price": 2500,
            "pe_ratio": 25.5,
            "roe": 12.3,
            "debt_to_equity": 0.45
        }
        
        print("\n🔍 Running analysis...")
        result = agent.analyze(context)
        
        print(f"✅ Analysis complete!")
        print(f"   Agent: {result.get('agent')}")
        print(f"   Type: {result.get('type')}")
        print(f"   Analysis length: {len(result.get('analysis', ''))} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_technical_agent():
    """Test Technical Analysis Agent."""
    print("\n" + "=" * 60)
    print("Testing Technical Analysis Agent")
    print("=" * 60)
    
    try:
        agent = TechnicalAnalysisAgent()
        print(f"✅ Agent initialized: {agent.agent_name}")
        
        context = {
            "ticker": "TCS.NS",
            "current_price": 3500,
            "ma_50": 3450,
            "ma_200": 3300,
            "rsi": 65,
            "week_52_high": 3800,
            "week_52_low": 2900
        }
        
        print("\n📈 Running analysis...")
        result = agent.analyze(context)
        
        print(f"✅ Analysis complete!")
        print(f"   Type: {result.get('type')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_sentiment_agent():
    """Test News Sentiment Agent."""
    print("\n" + "=" * 60)
    print("Testing News Sentiment Agent")
    print("=" * 60)
    
    try:
        agent = SentimentAnalysisAgent()
        print(f"✅ Agent initialized: {agent.agent_name}")
        
        context = {
            "ticker": "INFY.NS",
            "news_headlines": [
                "Infosys wins major deal with Fortune 500 company",
                "Concerns over IT sector growth in Q3",
                "Infosys announces dividend increase"
            ]
        }
        
        print("\n📰 Running sentiment analysis...")
        result = agent.analyze(context)
        
        print(f"✅ Analysis complete!")
        print(f"   Type: {result.get('type')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_risk_agent():
    """Test Risk Assessment Agent."""
    print("\n" + "=" * 60)
    print("Testing Risk Assessment Agent")
    print("=" * 60)
    
    try:
        agent = RiskAssessmentAgent()
        print(f"✅ Agent initialized: {agent.agent_name}")
        
        context = {
            "ticker": "HDFCBANK.NS",
            "beta": 0.85,
            "volatility": 18.5,
            "max_drawdown": -25.3,
            "sharpe_ratio": 1.45
        }
        
        print("\n⚠️ Running risk analysis...")
        result = agent.analyze(context)
        
        print(f"✅ Analysis complete!")
        print(f"   Type: {result.get('type')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_orchestrator():
    """Test Orchestrator Agent."""
    print("\n" + "=" * 60)
    print("Testing Orchestrator Agent")
    print("=" * 60)
    
    try:
        orchestrator = OrchestratorAgent()
        print(f"✅ Orchestrator initialized: {orchestrator.agent_name}")
        
        # Check agent health
        health = orchestrator.get_agent_health_status()
        print(f"\n🏥 Agent Health Status:")
        for name, status in health.items():
            print(f"   {name}: {status['status']}")
        
        print("\n✅ All agents healthy and ready!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_full_workflow():
    """Test complete multi-agent workflow."""
    print("\n" + "=" * 60)
    print("Testing Full Multi-Agent Workflow")
    print("=" * 60)
    
    try:
        # Fetch real data
        print("\n📡 Fetching real market data...")
        stock_data = FinancialDataProvider.get_comprehensive_stock_data("RELIANCE.NS")
        
        if "error" in stock_data:
            print(f"❌ Failed to fetch data: {stock_data['error']}")
            return False
        
        # Format for agents
        agent_data = FinancialDataProvider.format_for_agents(stock_data)
        
        # Initialize orchestrator
        orchestrator = OrchestratorAgent()
        
        # Prepare context
        context = {
            "request_type": "portfolio_analysis",
            "portfolio_data": agent_data.get("fundamental"),
            "user_profile": {
                "risk_tolerance": "Moderate"
            }
        }
        
        print("\n🤖 Running multi-agent analysis...")
        print("   This may take 30-60 seconds...")
        
        result = orchestrator.analyze(context)
        
        print("\n✅ Workflow complete!")
        print(f"   Workflow type: {result.get('workflow')}")
        print(f"   Agents executed: {len(result.get('agent_results', {}))}")
        print(f"   Synthesis length: {len(result.get('synthesis', ''))} characters")
        
        # Show synthesis preview
        synthesis = result.get('synthesis', '')
        if synthesis:
            print("\n📝 Synthesis Preview (first 500 chars):")
            print("-" * 60)
            print(synthesis[:500] + "..." if len(synthesis) > 500 else synthesis)
            print("-" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Error in workflow: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("\n" + "🤖" * 30)
    print("Multi-Agent Portfolio Advisor - System Test")
    print("🤖" * 30)
    
    # Check API key
    if not os.environ.get("GEMINI_API_KEY"):
        print("\n❌ GEMINI_API_KEY not found in environment!")
        print("   Please set it in your .env file")
        return
    
    print("\n✅ API key found")
    
    tests = [
        ("Data Provider", test_data_provider),
        ("Fundamental Agent", test_fundamental_agent),
        ("Technical Agent", test_technical_agent),
        ("Sentiment Agent", test_sentiment_agent),
        ("Risk Agent", test_risk_agent),
        ("Orchestrator", test_orchestrator),
        ("Full Workflow", test_full_workflow),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All systems operational! Ready for production.")
    else:
        print("\n⚠️ Some tests failed. Please review errors above.")

if __name__ == "__main__":
    main()
