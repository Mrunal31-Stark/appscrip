# FastAPI Market Analysis Service

A secure, high-performance API that provides real-time market insights and trade opportunities for specific sectors using AI.

## Tech Stack

This project is built using the following technologies:

- **Language**: Python 3.10+
- **Framework**: FastAPI (Asynchronous Web Framework)
- **Server**: Uvicorn (ASGI Server)
- **AI Engine**: Google Gemini (via `google-generativeai`)
- **Data Source**: DuckDuckGo Search (via `duckduckgo-search`)
- **Security**: Slowapi (Rate Limiting) & Custom API Key Middleware
- **Environment Management**: Python-dotenv

## Features

1. **Real-Time Data**: Fetches the latest market news and trends dynamically.
2. **AI Analysis**: Generates professional, structured trade opportunity reports.
3. **Secure**: Protected by API Key authentication and Rate Limiting.
4. **Auto-Save**: Automatically saves reports as `market_analysis_{sector}.md` files locally.

## Setup Instructions

### 1. clone and Install Dependencies

Ensure you have Python installed, then run:

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a file named `.env` in the root directory. Add the following configuration:

```ini
# Google Gemini API Key (Required for AI analysis)
GEMINI_API_KEY=your_actual_gemini_key_here

# Security Key (Required for API access)
API_SECRET_KEY=appscrip
```

### 3. Start the Server

Run the application using Uvicorn. Use port 8001:

```bash
uvicorn app.main:app --reload --port 8001
```

## Usage Guide

The API exposes a single endpoint to analyze market sectors.

**Endpoint**: `GET /analyze/{sector}`
**Header Required**: `x-api-key: appscrip`

### Example Request (PowerShell)

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8001/analyze/technology" -Method Get -Headers @{ "x-api-key" = "appscrip" }
```

### Example Request (Curl)

```bash
curl -X 'GET' \
  'http://127.0.0.1:8001/analyze/pharmaceuticals' \
  -H 'accept: application/json' \
  -H 'x-api-key: appscrip'
```

### Output

1. The API returns a JSON response containing the full Markdown report.
2. A file named `market_analysis_technology.md` (or relevant sector) is automatically created in your project folder.

## Troubleshooting

- **403 Forbidden**: Ensure your request header `x-api-key` matches the `API_SECRET_KEY` in your `.env` file.
- **System Busy**: If you receive a busy message, you have hit the Gemini Free Tier rate limit. Wait 60 seconds and try again.
