from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

from app.agent import get_stock_recommendation
from app.config import HOST, PORT

app = FastAPI(title="Stock Market AI Agent", 
              description="An API for getting stock prices and investment recommendations")

class StockRequest(BaseModel):
    ticker: str
    model: Optional[str] = None

@app.post("/stock-info")
async def stock_info(request: StockRequest):
    """Get stock information and recommendation for a ticker symbol"""
    try:
        result = get_stock_recommendation(request.ticker, request.model)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """API root endpoint with basic instructions"""
    return {
        "message": "Welcome to the Stock Market AI Agent API",
        "endpoints": {
            "/stock-info": "POST - Get stock information and recommendation"
        },
        "example": {
            "request": {"ticker": "AAPL", "model": "gpt-3.5-turbo"},
            "curl": 'curl -X POST "http://localhost:8000/stock-info" -H "Content-Type: application/json" -d \'{"ticker": "AAPL"}\''
        }
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)