"""
Setup RAG (Retrieval-Augmented Generation) System
Implements vector database for document retrieval
"""
import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import json
from datetime import datetime


class RAGSystem:
    """
    Complete RAG implementation with ChromaDB.
    
    Features:
    - Document indexing (annual reports, analyses, news)
    - Semantic search with embeddings
    - Metadata filtering
    - Source tracking
    """
    
    def __init__(self, persist_directory="./chroma_db"):
        """Initialize RAG system with ChromaDB."""
        
        print("🔧 Initializing RAG System...")
        
        # Initialize embedding model
        print("📥 Loading embedding model (all-MiniLM-L6-v2)...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Embedding model loaded")
        
        # Initialize ChromaDB client
        print(f"💾 Initializing ChromaDB at {persist_directory}...")
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        
        # Create collections for different document types
        self.collections = {
            "financial_reports": self._get_or_create_collection("financial_reports"),
            "stock_analyses": self._get_or_create_collection("stock_analyses"),
            "news_articles": self._get_or_create_collection("news_articles"),
            "research_reports": self._get_or_create_collection("research_reports"),
            "regulatory_docs": self._get_or_create_collection("regulatory_docs")
        }
        
        print("✅ RAG System initialized successfully!\n")
    
    def _get_or_create_collection(self, name: str):
        """Get existing collection or create new one."""
        try:
            return self.client.get_collection(name)
        except:
            return self.client.create_collection(
                name=name,
                metadata={"description": f"Collection for {name}"}
            )
    
    def index_document(self, 
                      text: str, 
                      doc_type: str,
                      metadata: Dict[str, Any]) -> str:
        """
        Index a single document.
        
        Args:
            text: Document content
            doc_type: Type (financial_reports, stock_analyses, etc.)
            metadata: Additional metadata (ticker, date, source, etc.)
        
        Returns:
            Document ID
        """
        collection = self.collections.get(doc_type)
        if not collection:
            raise ValueError(f"Unknown doc_type: {doc_type}")
        
        # Generate embedding
        embedding = self.embedding_model.encode(text).tolist()
        
        # Create document ID
        doc_id = f"{doc_type}_{metadata.get('ticker', 'general')}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Add to collection
        collection.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[doc_id]
        )
        
        return doc_id
    
    def retrieve(self, 
                query: str, 
                doc_types: List[str] = None,
                n_results: int = 5,
                filter_metadata: Dict = None) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: Search query
            doc_types: Which collections to search (None = all)
            n_results: Number of results to return
            filter_metadata: Metadata filters (e.g., {"ticker": "RELIANCE.NS"})
        
        Returns:
            List of relevant documents with metadata
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Search collections
        if doc_types is None:
            doc_types = list(self.collections.keys())
        
        all_results = []
        
        for doc_type in doc_types:
            collection = self.collections[doc_type]
            
            # Query with filters
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=filter_metadata
            )
            
            # Format results
            for i in range(len(results['documents'][0])):
                all_results.append({
                    "doc_type": doc_type,
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "relevance_score": 1 - results['distances'][0][i],  # Convert distance to similarity
                    "id": results['ids'][0][i]
                })
        
        # Sort by relevance
        all_results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return all_results[:n_results]
    
    def index_stock_analysis(self, 
                            ticker: str,
                            analysis: str,
                            agent_type: str,
                            rating: str,
                            date: str = None):
        """Index a stock analysis for future retrieval."""
        metadata = {
            "ticker": ticker,
            "agent_type": agent_type,
            "rating": rating,
            "date": date or datetime.now().strftime("%Y-%m-%d"),
            "source": "multi_agent_system"
        }
        
        return self.index_document(
            text=analysis,
            doc_type="stock_analyses",
            metadata=metadata
        )
    
    def get_past_analyses(self, ticker: str, limit: int = 3) -> List[Dict]:
        """Get past analyses for a specific ticker."""
        return self.retrieve(
            query=f"Analysis of {ticker}",
            doc_types=["stock_analyses"],
            n_results=limit,
            filter_metadata={"ticker": ticker}
        )
    
    def stats(self) -> Dict[str, int]:
        """Get collection statistics."""
        stats = {}
        for name, collection in self.collections.items():
            stats[name] = collection.count()
        return stats


def demo_rag_system():
    """Demo: Index some sample documents and retrieve them."""
    
    print("=" * 60)
    print("RAG SYSTEM DEMO")
    print("=" * 60)
    
    # Initialize RAG
    rag = RAGSystem(persist_directory="./demo_chroma_db")
    
    # Index some sample documents
    print("\n📚 Indexing sample documents...")
    
    # Sample: Stock analysis
    rag.index_stock_analysis(
        ticker="RELIANCE.NS",
        analysis="""
        RELIANCE.NS shows strong fundamentals with ROE of 12.3% and revenue growth of 18%.
        P/E of 25.5 is slightly above sector average. Conservative debt management with D/E of 0.45.
        Rating: HOLD. Target Price: ₹2,300. Confidence: HIGH.
        Key risks include crude oil volatility and regulatory challenges in telecom.
        """,
        agent_type="fundamental",
        rating="HOLD"
    )
    
    rag.index_stock_analysis(
        ticker="TCS.NS",
        analysis="""
        TCS.NS demonstrates premium quality with ROE of 42% and consistent growth.
        P/E of 28x justified by best-in-class profitability. Defensive IT sector play.
        Rating: BUY. Target Price: ₹3,800. Confidence: HIGH.
        Risks include currency headwinds and valuation risk if sector derates.
        """,
        agent_type="fundamental",
        rating="BUY"
    )
    
    # Sample: Financial report
    rag.index_document(
        text="""
        RELIANCE Industries Annual Report 2025:
        - Consolidated revenue: ₹9.2 trillion (up 18% YoY)
        - EBITDA margin improved to 14.2%
        - Net debt reduced by ₹45,000 crores
        - Digital services (Jio) now contributing 30% of EBITDA
        - Retail expansion: 5,000+ new stores opened
        - Focus on green energy transition with ₹75,000 crore investment plan
        """,
        doc_type="financial_reports",
        metadata={
            "ticker": "RELIANCE.NS",
            "report_type": "annual_report",
            "year": 2025,
            "source": "company_website"
        }
    )
    
    # Sample: Tax guideline
    rag.index_document(
        text="""
        Indian Capital Gains Tax Rules (2026):
        - LTCG (holding >1 year): 12.5% tax above ₹1.25 lakh exemption
        - STCG (holding <1 year): 20% flat tax
        - Dividends: Taxed at individual's slab rate
        - Tax Loss Harvesting: Losses can offset gains in same financial year
        - Section 80C: Up to ₹1.5 lakh deduction for ELSS investments
        """,
        doc_type="regulatory_docs",
        metadata={
            "type": "tax_guidelines",
            "year": 2026,
            "source": "Income_Tax_Act"
        }
    )
    
    print(f"✅ Indexed {sum(rag.stats().values())} documents")
    print(f"   Distribution: {rag.stats()}")
    
    # Retrieve documents
    print("\n🔍 Testing retrieval...")
    
    # Query 1: General query
    print("\n1️⃣ Query: 'RELIANCE financial performance'")
    results = rag.retrieve("RELIANCE financial performance", n_results=2)
    for i, doc in enumerate(results, 1):
        print(f"\n   Result {i} (Relevance: {doc['relevance_score']:.2f}):")
        print(f"   Type: {doc['doc_type']}")
        print(f"   Content: {doc['content'][:150]}...")
    
    # Query 2: Specific ticker
    print("\n2️⃣ Query: 'Past analyses for TCS.NS'")
    results = rag.get_past_analyses("TCS.NS")
    for i, doc in enumerate(results, 1):
        print(f"\n   Analysis {i}:")
        print(f"   Rating: {doc['metadata'].get('rating')}")
        print(f"   Date: {doc['metadata'].get('date')}")
        print(f"   Content: {doc['content'][:150]}...")
    
    # Query 3: Tax information
    print("\n3️⃣ Query: 'Tax implications for long-term investments'")
    results = rag.retrieve(
        "Tax implications for long-term investments",
        doc_types=["regulatory_docs"],
        n_results=1
    )
    if results:
        print(f"\n   {results[0]['content']}")
    
    print("\n" + "=" * 60)
    print("✅ RAG System Demo Complete!")
    print("=" * 60)


def setup_production_rag():
    """Setup RAG for production use."""
    
    print("🏗️  Setting up RAG for production...")
    
    # Initialize
    rag = RAGSystem(persist_directory="./chroma_db")
    
    print(f"""
✅ RAG System Ready!

Next steps:
1. Index your documents:
   python scripts/index_documents.py
   
2. Integrate with agents:
   from scripts.setup_rag import RAGSystem
   rag = RAGSystem()
   results = rag.retrieve("your query")
   
3. Update analyses automatically:
   After each analysis, index it for future retrieval

Collections created:
{chr(10).join([f'  • {name}: {collection.count()} documents' for name, collection in rag.collections.items()])}
""")
    
    return rag


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        # Run demo
        demo_rag_system()
    else:
        # Setup for production
        setup_production_rag()
