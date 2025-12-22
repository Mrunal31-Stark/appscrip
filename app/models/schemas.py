from pydantic import BaseModel

class AnalysisRequest(BaseModel):
    sector: str

class AnalysisResponse(BaseModel):
    sector: str
    report_markdown: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "sector": "technology",
                "report_markdown": "# Market Analysis for Technology\n\n..."
            }
        }
