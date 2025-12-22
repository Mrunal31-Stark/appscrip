class MarketAnalysisError(Exception):
    """Base error for analysis failures"""
    def __init__(self, message: str):
        self.message = message
