import google.generativeai as genai
from app.config import settings
from app.core.exceptions import MarketAnalysisError

class AnalysisService:
    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set")
        
        genai.configure(api_key=settings.GEMINI_API_KEY)
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def analyze_market_opportunities(self, sector: str, market_data: str) -> str:
        """
        Sends the collected market data to Gemini to generate a structured report.
        """
        prompt = f"""
        Act as a senior financial analyst. 
        Analyze the following collected market data for the '{sector}' sector in India.
        
        Data:
        {market_data}
        
        Task:
        Identify current trade opportunities and market trends.
        
        Output Format:
        Provide the response in clean Markdown format with the following sections:
        
        # Market Analysis: {sector.capitalize()}
        
        ## 1. Executive Summary
        (Brief overview of the current state)
        
        ## 2. Key Trends
        (Bulleted list of major movements)
        
        ## 3. Trade Opportunities
        (Specific actionable insights)
        
        ## 4. Risks & Considerations
        
        Note: Be professional, concise, and highlight actionable insights.
        """
        
        try:
            print(f"Analyzing with Gemini 2.5 Flash...")
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "Resource has been exhausted" in error_msg:
                print("Hit Gemini Free Tier Rate Limit.")
                return "# System Busy\n\nThe AI service is currently experiencing high traffic (Free Tier Quota Exceeded). Please try again in 1 minute."
            
            print(f"Gemini Analysis Error: {e}")
            raise MarketAnalysisError(f"AI Analysis failed: {str(e)}")

# Initialize strictly when needed or handle initialization errors gracefully in main
# I have instantiate this inside the dependency to avoid startup errors if key is missing during tests
