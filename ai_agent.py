import os
from google import genai
from google.genai import types

def get_gemini_client():
    """Initializes and returns the Gemini client."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in your .env file.")
    return genai.Client(api_key=api_key)

def analyze_portfolio(portfolio_data: str) -> str:
    """Analyzes the current portfolio based on fetched financial data."""
    client = get_gemini_client()
    
    prompt = f"""
    You are an expert AI financial analyst. I am going to provide you with raw financial data and recent news headlines for a user's current investment portfolio.
    
    Your job is to provide a clear, 'Explain Like I'm 5' (ELI5) analysis of their current holdings. 
    
    For each asset:
    1. Summarize how the company is doing based on the business summary.
    2. Analyze the recent news and provide a 'Short-Term Sentiment' (Bullish, Bearish, or Neutral) and explain why.
    3. Identify any major risks or disconnects (e.g., if the stock is up but news is bad, or vice versa).
    
    Here is the portfolio data:
    {portfolio_data}
    
    Format your response clearly using Markdown headings and bullet points.
    """
    
    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt,
    )
    return response.text

def suggest_investments(portfolio_tickers: list, corpus: float, preferences: str) -> str:
    """Suggests new investments based on user preferences and corpus."""
    client = get_gemini_client()
    
    prompt = f"""
    You are an expert AI financial wealth advisor for the Indian market.
    
    The user currently holds the following assets: {', '.join(portfolio_tickers) if portfolio_tickers else 'None'}.
    The user has an available investment corpus of: ₹{corpus:,.2f}.
    The user has the following investment preferences and risk appetite: "{preferences}"
    
    Based on their corpus and preferences, suggest 3 to 5 new investment options (Stocks or ETFs, preferably traded on NSE/BSE).
    
    For each suggestion:
    1. Provide the ticker symbol (using .NS or .BO suffix where applicable).
    2. Explain *why* it fits their specific preferences.
    3. Briefly mention the primary risk associated with this investment.
    
    Important: Include a standard disclaimer that this is AI-generated advice for educational purposes and not professional financial advice.
    Format your response clearly using Markdown.
    """
    
    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt,
    )
    return response.text
