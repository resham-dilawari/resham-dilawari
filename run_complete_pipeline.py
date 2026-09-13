"""
Complete Pipeline: RAG + Training Data + Evaluation
Demonstrates the full workflow for improving agents
"""
import os
import sys
from datetime import datetime


def print_header(text: str):
    """Print formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def check_dependencies():
    """Check if all required packages are installed."""
    print_header("1. CHECKING DEPENDENCIES")
    
    required_packages = {
        "chromadb": "RAG functionality",
        "sentence_transformers": "Text embeddings for RAG",
        "yfinance": "Financial data",
        "google.genai": "Gemini API"
    }
    
    missing = []
    
    for package, purpose in required_packages.items():
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package:25} - {purpose}")
        except ImportError:
            print(f"❌ {package:25} - {purpose} (MISSING)")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print(f"   Install with: pip install {' '.join(missing)}")
        return False
    
    print("\n✅ All dependencies installed!")
    return True


def setup_rag():
    """Setup RAG system."""
    print_header("2. SETTING UP RAG SYSTEM")
    
    try:
        from scripts.setup_rag import RAGSystem, demo_rag_system
        
        print("Running RAG demo...")
        demo_rag_system()
        
        print("\n✅ RAG system ready!")
        return True
        
    except Exception as e:
        print(f"❌ Error setting up RAG: {e}")
        import traceback
        traceback.print_exc()
        return False


def generate_training_data():
    """Generate training data for fine-tuning."""
    print_header("3. GENERATING TRAINING DATA")
    
    try:
        from scripts.prepare_training_data import TrainingDataGenerator
        
        generator = TrainingDataGenerator()
        
        print("Generating training examples...")
        print("(Using small sample size for demo - increase for production)")
        
        examples = generator.generate_training_dataset(
            num_examples_per_agent=10,  # Small for demo
            agents=["fundamental", "technical", "risk"]
        )
        
        generator.save_training_data(examples, "demo_training_data.jsonl")
        
        print(f"\n✅ Generated {len(examples)} training examples!")
        print(f"   Saved to: demo_training_data.jsonl")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating training data: {e}")
        import traceback
        traceback.print_exc()
        return False


def evaluate_agents():
    """Evaluate agent performance."""
    print_header("4. EVALUATING AGENTS")
    
    try:
        # Check API key first
        if not os.environ.get("GEMINI_API_KEY"):
            print("⚠️  GEMINI_API_KEY not set - skipping agent evaluation")
            print("   Set API key in .env file to run evaluations")
            return False
        
        from scripts.evaluate_agents import AgentEvaluator, compare_agents
        from agents.fundamental_agent import FundamentalAnalysisAgent
        from agents.technical_agent import TechnicalAnalysisAgent
        from agents.risk_agent import RiskAssessmentAgent
        
        agents_to_test = [
            (FundamentalAnalysisAgent(), "Fundamental Agent"),
            (TechnicalAnalysisAgent(), "Technical Agent"),
            (RiskAssessmentAgent(), "Risk Agent")
        ]
        
        all_results = []
        
        for agent, name in agents_to_test:
            print(f"\nEvaluating {name}...")
            evaluator = AgentEvaluator(agent, name)
            results = evaluator.run_all_tests()
            all_results.append(results)
        
        # Compare
        if len(all_results) > 1:
            compare_agents(all_results)
        
        print("\n✅ Evaluation complete!")
        return True
        
    except Exception as e:
        print(f"❌ Error evaluating agents: {e}")
        import traceback
        traceback.print_exc()
        return False


def show_next_steps():
    """Show what to do next."""
    print_header("5. NEXT STEPS")
    
    print("""
📚 You've completed the setup! Here's what you can do next:

1️⃣  IMPROVE PROMPTS (Easiest, do this first!)
   📄 Read: docs/PROMPTS.md
   🔧 Modify prompts in agents/*.py
   🧪 Test with: python demo_agents.py
   
2️⃣  USE RAG IN PRODUCTION
   📝 Index your documents:
      - Annual reports
      - Past analyses
      - Research reports
   
   💻 Code:
      from scripts.setup_rag import RAGSystem
      rag = RAGSystem()
      results = rag.retrieve("your query")
   
3️⃣  FINE-TUNE AGENTS
   📊 Generate 1000+ examples:
      python scripts/prepare_training_data.py --count=1000
   
   🎓 Fine-tune with Gemini API:
      # Upload training_data.jsonl to Gemini
      # Start fine-tuning job
      # Get fine-tuned model name
   
   📄 Guide: docs/FINE_TUNING_AND_EVALS.md
   
4️⃣  CONTINUOUS EVALUATION
   🧪 Run evals regularly:
      python scripts/evaluate_agents.py
   
   📊 Track metrics:
      - Recommendation accuracy
      - User satisfaction
      - Format consistency
   
   📈 Compare before/after fine-tuning
   
5️⃣  PRODUCTION DEPLOYMENT
   🚀 Deploy to Streamlit Cloud
   📱 Build mobile app
   🔗 Integrate with broker APIs
   💰 Add monetization

📖 DOCUMENTATION CREATED:
   • docs/WHAT_IS_FINE_TUNING.md - Complete explanation
   • docs/PROMPTS.md - All system prompts
   • docs/FINE_TUNING_AND_EVALS.md - Complete guide
   • docs/RAG_FINETUNING_PROMPTS_SUMMARY.md - Quick reference
   • agents/rag_agent.py - RAG implementation
   • scripts/setup_rag.py - RAG setup
   • scripts/prepare_training_data.py - Training data generation
   • scripts/evaluate_agents.py - Evaluation framework

🎯 RECOMMENDED ORDER:
   Week 1: Optimize prompts (biggest ROI)
   Week 2-3: Add RAG (moderate effort, high value)
   Month 2: Fine-tune (highest accuracy)
   Ongoing: Continuous evaluation

💡 QUICK WINS:
   • Modify one prompt → Test → Deploy (30 min)
   • Index 10 annual reports → Better context (2 hours)
   • Generate training data → Prepare for fine-tuning (4 hours)
   • Run full evaluation → Know your baseline (1 hour)
""")


def main():
    """Run complete pipeline."""
    
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   COMPLETE PIPELINE: RAG + FINE-TUNING + EVALUATION             ║
║   Multi-Agent AI Portfolio Advisor                               ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
""")
    
    # Track what succeeded
    results = {
        "dependencies": False,
        "rag": False,
        "training_data": False,
        "evaluation": False
    }
    
    # Step 1: Check dependencies
    results["dependencies"] = check_dependencies()
    if not results["dependencies"]:
        print("\n⚠️  Please install missing dependencies first")
        print("   Run: pip install -r requirements.txt")
        return
    
    # Step 2: Setup RAG
    print("\n" + "─" * 70)
    user_input = input("\nSetup RAG system? (y/n): ")
    if user_input.lower() == 'y':
        results["rag"] = setup_rag()
    else:
        print("⏭️  Skipping RAG setup")
    
    # Step 3: Generate training data
    print("\n" + "─" * 70)
    user_input = input("\nGenerate training data? (y/n): ")
    if user_input.lower() == 'y':
        results["training_data"] = generate_training_data()
    else:
        print("⏭️  Skipping training data generation")
    
    # Step 4: Evaluate agents
    print("\n" + "─" * 70)
    user_input = input("\nEvaluate agents? (requires API key) (y/n): ")
    if user_input.lower() == 'y':
        results["evaluation"] = evaluate_agents()
    else:
        print("⏭️  Skipping agent evaluation")
    
    # Show next steps
    show_next_steps()
    
    # Summary
    print_header("PIPELINE SUMMARY")
    print(f"✅ Dependencies: {'Ready' if results['dependencies'] else 'Failed'}")
    print(f"{'✅' if results['rag'] else '⏭️'} RAG System: {'Setup' if results['rag'] else 'Skipped'}")
    print(f"{'✅' if results['training_data'] else '⏭️'} Training Data: {'Generated' if results['training_data'] else 'Skipped'}")
    print(f"{'✅' if results['evaluation'] else '⏭️'} Evaluation: {'Complete' if results['evaluation'] else 'Skipped'}")
    
    print("\n🎉 Pipeline complete! Check the 'NEXT STEPS' section above.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
