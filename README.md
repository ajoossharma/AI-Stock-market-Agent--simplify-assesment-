# Stock Market AI Agent

This project is an AI-powered stock market agent that provides stock price information and investment recommendations through a REST API.

## Features

- Fetch real-time stock market prices
- Get historical stock price data
- Receive AI-generated investment recommendations (Buy/Sell/Hold)
- RESTful API for easy integration

## Prerequisites

- Python 3.8+
- OpenAI API key

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/stock-market-agent.git
cd stock-market-agent
```

2. Create a virtual environment and activate it
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root directory with your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
DEFAULT_MODEL=gpt-3.5-turbo
PORT=8000
```

## Usage

1. Start the API server:
```bash
python main.py
```

2. Access the API at `http://localhost:8000`

3. Example API request using curl:
```bash
curl -X POST "http://localhost:8000/stock-info" \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL"}'
```

4. Example API request using Python requests:
```python
import requests

response = requests.post("http://localhost:8000/stock-info", 
                        json={"ticker": "AAPL"})
print(response.json())
```

## Deployment

### Deploy on Render

1. Sign up for a free [Render](https://render.com/) account
2. Create a new Web Service
3. Connect your GitHub repository
4. Set the following options:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add your environment variables (OPENAI_API_KEY, etc.) in the Render dashboard

### Deploy on Railway

1. Sign up for [Railway](https://railway.app/)
2. Create a new project from GitHub
3. Select your repository
4. Add environment variables
5. Railway will automatically deploy your application

## API Endpoints

### GET /

Returns basic information about the API.

### POST /stock-info

Get stock information and recommendation for a ticker symbol.

**Request Body:**
```json
{
  "ticker": "AAPL",
  "model": "gpt-3.5-turbo"  
}
```

**Response:**
```json
{
  "response": "The current price of Apple Inc. (AAPL) is $188.63 USD. Based on recent performance and financial metrics, I would recommend a BUY. The company shows strong fundamentals with a market cap of $2.94T, a PE ratio of 29.4, and a dividend yield of 0.5%. The stock is trading closer to its 52-week low ($158.77) than its high ($227.94), potentially offering good value. Recent product announcements and consistent revenue growth support this recommendation."
}
```

## Project Structure

```
stock_market_agent/
├── .env                  # Environment variables (API keys)
├── requirements.txt      # Dependencies
├── main.py               # FastAPI application entry point
├── README.md             # Documentation
└── app/
    ├── __init__.py
    ├── agent.py          # LangChain agent implementation
    ├── tools/
    │   ├── __init__.py
    │   └── stock_tools.py  # Tools for stock data retrieval
    └── config.py         # Configuration settings
```

## License

MIT
