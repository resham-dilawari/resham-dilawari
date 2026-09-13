"""
Quick RAG Database Setup (Lightweight)
Creates the database structure without waiting for large downloads
"""
import os
import json
from datetime import datetime

def create_simple_db():
    """Create a simple JSON-based knowledge base as fallback."""
    
    print("🚀 Creating lightweight knowledge base...")
    
    # Create directory
    db_dir = "./simple_rag_db"
    os.makedirs(db_dir, exist_ok=True)
    
    # Sample documents
    documents = {
        "stock_analyses": [
            {
                "ticker": "RELIANCE.NS",
                "date": "2025-12-01",
                "analysis": """**RELIANCE Industries Analysis**
                
Strong fundamentals with diversified revenue streams. O2C segment provides stable cash flows.
Key Metrics: P/E 24.5x, ROE 12.8%, D/E 0.45
Rating: HOLD | Target: ₹2,800 | Confidence: HIGH
""",
                "agent": "fundamental_agent"
            },
            {
                "ticker": "TCS.NS",
                "date": "2025-11-15",
                "analysis": """**TCS - IT Sector Leader**
                
Defensive play with consistent performance. Industry-leading margins of 25%.
Key Metrics: P/E 28.5x, ROE 45%, Debt-free
Rating: BUY for long-term | Target: ₹4,200 | Risk: LOW
""",
                "agent": "fundamental_agent"
            },
            {
                "ticker": "HDFCBANK.NS",
                "date": "2025-12-05",
                "analysis": """**HDFC Bank Post-Merger**
                
Integration challenges being managed. Scale benefits emerging.
Key Metrics: P/E 19.5x, CASA 42%, NPA 1.1%
Rating: ACCUMULATE | Target: ₹1,850 | Risk: MEDIUM
""",
                "agent": "fundamental_agent"
            }
        ],
        "tax_rules": [
            {
                "topic": "Capital Gains Tax",
                "content": """**Indian Tax Rules 2026**
                
LTCG (>12 months): 12.5% on gains above ₹1.25L
STCG (≤12 months): 20% flat rate
Tax Loss Harvesting: Losses can offset gains, carry forward 8 years
Section 80C: ELSS qualifies, ₹1.5L max deduction
"""
            }
        ],
        "risk_frameworks": [
            {
                "topic": "Portfolio Risk Management",
                "content": """**Risk Classification**
                
LOW RISK: Volatility <15%, Beta 0.5-0.8, 70-80% allocation
MEDIUM RISK: Volatility 15-25%, Beta 0.8-1.2, 50-60% allocation  
HIGH RISK: Volatility >25%, Beta >1.2, 20-30% allocation

Diversification: 8-15 stocks, no single stock >20%, no sector >30%
"""
            }
        ],
        "sector_research": [
            {
                "sector": "Information Technology",
                "date": "2025-12-01",
                "content": """**IT Sector Outlook**
                
Expected to reach $250B by FY26, growing at 12-15% CAGR.
Digital services now 65% of revenue. Strong deal pipeline.
Sector Rating: OVERWEIGHT | Avg P/E: 25x
Prefer: TCS, Infosys for stability; Mid-caps for growth
"""
            }
        ]
    }
    
    # Save to JSON
    with open(f"{db_dir}/knowledge_base.json", "w") as f:
        json.dump(documents, f, indent=2)
    
    # Create metadata
    metadata = {
        "created": datetime.now().isoformat(),
        "total_documents": sum(len(docs) for docs in documents.values() if isinstance(docs, list)),
        "collections": list(documents.keys()),
        "status": "active"
    }
    
    with open(f"{db_dir}/metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✅ Database created at: {os.path.abspath(db_dir)}")
    print(f"📊 Total documents: {metadata['total_documents']}")
    print(f"📁 Collections: {', '.join(metadata['collections'])}")
    print(f"\n🎉 Lightweight RAG ready!")
    
    return db_dir

def show_db_location():
    """Show where databases will be stored."""
    print("\n" + "=" * 60)
    print("📍 DATABASE LOCATIONS")
    print("=" * 60)
    
    project_root = os.path.abspath(".")
    
    print(f"\n1️⃣  **Full ChromaDB** (when embedding model downloads):")
    print(f"   Path: {os.path.join(project_root, 'chroma_db')}")
    print(f"   Status: ⏳ Waiting for sentence-transformers download")
    print(f"   Size: ~500MB (includes embedding model)")
    
    print(f"\n2️⃣  **Simple JSON DB** (lightweight fallback):")
    print(f"   Path: {os.path.join(project_root, 'simple_rag_db')}")
    print(f"   Status: ✅ Ready to create")
    print(f"   Size: ~50KB")
    
    print(f"\n3️⃣  **Demo DB** (for testing):")
    print(f"   Path: {os.path.join(project_root, 'demo_chroma_db')}")
    print(f"   Status: Created only when running setup_rag.py --demo")
    
    print("\n" + "=" * 60)
    print("💡 TIP: The app works with mock RAG data until DB is ready")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    show_db_location()
    
    print("\n🔧 Creating simple knowledge base...\n")
    db_path = create_simple_db()
    
    print(f"\n✨ You can now use the app! RAG will use this lightweight DB.")
    print(f"   When ChromaDB finishes downloading, run: python scripts\\index_sample_data.py")
