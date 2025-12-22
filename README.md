# FastAPI Market Analysis Service

A secure, high-performance API that provides real-time market insights and trade opportunities for specific sectors using AI. Now features a premium **Web Interface**.

## Tech Stack

This project is built using the following technologies:

- **Language**: Python 3.10+
- **Framework**: FastAPI (Asynchronous Web Framework)
- **Frontend**: HTML5, CSS3 (Glassmorphism), JavaScript (Vanilla)
- **AI Engine**: Google Gemini (via `google-generativeai`)
- **Data Source**: DuckDuckGo Search (via `duckduckgo-search`)
- **Security**: Slowapi (Rate Limiting) & Custom API Key Middleware

## Features

1.  **Web Interface**: Beautiful dark-mode UI to analyze markets and download reports.
2.  **Real-Time Data**: Fetches the latest market news and trends dynamically.
3.  **AI Analysis**: Generates professional, structured trade opportunity reports.
4.  **Secure**: Protected by API Key authentication and Rate Limiting.
5.  **Auto-Save**: Automatically saves reports as `market_analysis_{sector}.md` files locally.

## Setup Instructions

### 1. Clone and Install Dependencies

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

### 🌐 Web Interface (Recommended)
1.  Open your browser to `http://127.0.0.1:8001`.
2.  Enter the Sector Name (e.g., "Crypto").
3.  Enter the API Key (`appscrip`).
4.  Click **Analyze** and then **Download Report**.

### 🔌 API Endpoint

**Endpoint**: `GET /analyze/{sector}`
**Header Required**: `x-api-key: appscrip`

**Example Request:**
```bash
curl -X 'GET' \
  'http://127.0.0.1:8001/analyze/pharmaceuticals' \
  -H 'accept: application/json' \
  -H 'x-api-key: appscrip'
```

## Troubleshooting

- **403 Forbidden**: Ensure your request header `x-api-key` matches the `API_SECRET_KEY` in your `.env` file.
- **System Busy**: If you receive a busy message, you have hit the Gemini Free Tier rate limit. Wait 60 seconds and try again.
