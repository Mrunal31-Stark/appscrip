from duckduckgo_search import DDGS
from app.core.exceptions import MarketAnalysisError

class MarketDataService:
    def __init__(self):
        self.ddgs = DDGS()

    def get_sector_news(self, sector: str, max_results: int = 5) -> str:  # Searches for recent news and market data for the given sectorReturns a compiled string of titles and snippets.
        
        query = f"latest market trends trade opportunities {sector} sector India"
        try:
            results = self.ddgs.text(query, max_results=max_results)
            
            if not results:
                return f"No specific market data found for {sector}."

            compiled_data = f"Market Data for {sector}:\n\n"
            for i, res in enumerate(results, 1):
                compiled_data += f"{i}. {res['title']}\n   Source: {res['href']}\n   Snippet: {res['body']}\n\n"
            
            return compiled_data
            
        except Exception as e:
            # Log the error in a real app
            print(f"Error fetching data: {e}")
            raise MarketAnalysisError(f"Failed to fetch market data: {str(e)}")

market_service = MarketDataService()
