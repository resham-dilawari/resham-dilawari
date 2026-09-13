import streamlit as st
from dotenv import load_dotenv
import os
import financial_data
import ai_agent

# Load environment variables (API Keys)
load_dotenv()

st.set_page_config(page_title="AI Portfolio Advisor", page_icon="📈", layout="wide")

st.title("📈 AI Portfolio Advisor (Indian Market)")
st.markdown("Analyze your current holdings and get AI-powered investment suggestions.")

# Sidebar for inputs
with st.sidebar:
    st.header("Your Profile")
    
    # Portfolio input
    st.subheader("Current Portfolio")
    portfolio_input = st.text_input(
        "Enter Stock Tickers (comma separated)", 
        placeholder="e.g., RELIANCE.NS, TCS.NS, INFY.BO",
        help="Use .NS for NSE and .BO for BSE"
    )
    
    # Corpus input
    st.subheader("Investment Corpus")
    corpus = st.number_input(
        "Available amount to invest (₹)", 
        min_value=0.0, 
        value=50000.0,
        step=5000.0
    )
    
    # Preferences input
    st.subheader("Preferences")
    preferences = st.text_area(
        "Investment Preferences & Risk Appetite", 
        placeholder="e.g., I want low risk dividend paying stocks, mostly in the IT sector.",
        height=100
    )
    
    analyze_button = st.button("Analyze & Suggest", type="primary")

# Main content area
if analyze_button:
    # Validate API Key
    if not os.environ.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY") == "your_api_key_here":
        st.error("⚠️ GEMINI_API_KEY is not set. Please add it to your .env file.")
        st.stop()
        
    tickers = [t.strip() for t in portfolio_input.split(",") if t.strip()]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Current Portfolio Analysis")
        if not tickers:
            st.info("No current portfolio provided. Skipping analysis.")
        else:
            with st.spinner("Fetching market data and news..."):
                aggregated_data = ""
                for ticker in tickers:
                    st.toast(f"Fetching data for {ticker}...")
                    aggregated_data += financial_data.get_full_stock_profile(ticker)
            
            if aggregated_data:
                with st.spinner("AI is analyzing your portfolio..."):
                    try:
                        analysis_result = ai_agent.analyze_portfolio(aggregated_data)
                        st.markdown(analysis_result)
                    except Exception as e:
                        st.error(f"Error during AI analysis: {e}")
            else:
                st.warning("Could not fetch data for the provided tickers.")

    with col2:
        st.header("AI Investment Suggestions")
        if not preferences:
            st.info("Please provide your investment preferences in the sidebar to get suggestions.")
        else:
            with st.spinner("AI is generating tailored suggestions..."):
                try:
                    suggestions_result = ai_agent.suggest_investments(tickers, corpus, preferences)
                    st.markdown(suggestions_result)
                except Exception as e:
                    st.error(f"Error during AI suggestions: {e}")
else:
    st.info("👈 Fill out your profile in the sidebar and click 'Analyze & Suggest' to begin.")
