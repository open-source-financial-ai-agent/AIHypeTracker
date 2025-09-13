#!/usr/bin/env python3.13
"""
Startup script for Financial Investment Analyzer Frontend
"""

import uvicorn
import sys
import os

# Add paths
sys.path.insert(0, '.venv_current/lib/python3.13/site-packages')
sys.path.insert(0, '.')

from dotenv import load_dotenv
load_dotenv('multi_tool_agent/.env')

from frontend_app import app

if __name__ == "__main__":
    print("🌟 Starting Financial Investment Analyzer Frontend")
    print("=" * 60)
    print("🔧 Features:")
    print("  ✅ Company search with contracted companies discovery")
    print("  ✅ Public trading status verification")
    print("  ✅ Financial metrics analysis with profit margins")
    print("  ✅ Interactive data visualizations with Chart.js")
    print("  ✅ Responsive modern UI with real-time data")
    print()
    print("🌐 Server will be available at:")
    print("  Frontend: http://localhost:8002")
    print("  API Docs: http://localhost:8002/docs")
    print()
    print("🔄 Backend Services:")
    print("  - FastAPI server with our financial agent")
    print("  - Real-time Gemini web search")
    print("  - yfinance financial data integration")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8002,
        reload=False,
        log_level="info"
    )