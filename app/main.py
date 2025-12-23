from fastapi import FastAPI, Depends, Request, HTTPException
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.config import settings
from app.core.security import limiter, verify_api_key
from app.core.exceptions import MarketAnalysisError
from app.services.market_data import market_service
from app.services.analysis import AnalysisService
from app.models.schemas import AnalysisResponse

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ... (imports remain)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API for collecting market data and generating trade opportunity reports."
)

# Initialize Rate Limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Mount Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    """Serve the Web UI."""
    return FileResponse('static/index.html')

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "active", "version": settings.VERSION}

@app.get("/analyze/{sector}", response_model=AnalysisResponse)
@limiter.limit("5/minute")
async def analyze_sector(
    request: Request,
    sector: str,
    api_key: str = Depends(verify_api_key)
):
    """
    Analyzes a specific sector.
    1. Fetches market data (DuckDuckGo).
    2. Generates AI report (Gemini).
    3. Saves report to 'market_analysis_report.md'.
    4. Returns markdown.
    
    Requires 'x-api-key' header.
    Rate limited to 5 requests per minute.
    """
    try:
        # Step 1: Collect Data
        print(f"Fetching data for: {sector}")
        market_data = market_service.get_sector_news(sector)
        
        # Step 2: Analyze Data
        # Initialize service here to handle lazy loading of API key
        analysis_service = AnalysisService() 
        print(f"Analyzing data with Gemini...")
        report_markdown = await analysis_service.analyze_market_opportunities(sector, market_data)
        
        # Step 3: Save to File (Local Dev Only)
        # Sanitize sector name for filename (remove spaces, special chars)
        safe_sector_name = "".join(c for c in sector if c.isalnum() or c in (' ', '-', '_')).strip().replace(' ', '_')
        file_path = f"market_analysis_{safe_sector_name}.md"
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(report_markdown)
            print(f"Report saved to {file_path}")
        except OSError:
            # Vercel/Serverless environments are Read-Only.
            print("Skipped saving file (Read-Only File System detected).")

        return AnalysisResponse(
            sector=sector,
            report_markdown=report_markdown
        )
        
    except MarketAnalysisError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except ValueError as e:
        # Likely missing API key configuration
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)
