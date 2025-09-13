# Contracted Companies Analyzer Agent

An AI agent that finds contracted companies for big tech companies and analyzes their public trading status for investment opportunities.

## 🚀 How to Run

### Quick Demo
```bash
./.venv_current/bin/python3.13 demo.py
```

### Interactive Mode
```bash
./.venv_current/bin/python3.13 run_agent.py
```

### Direct Function Usage
```bash
./.venv_current/bin/python3.13 -c "
import sys
sys.path.insert(0, '.venv_current/lib/python3.13/site-packages')
sys.path.insert(0, 'multi_tool_agent')
from dotenv import load_dotenv
load_dotenv('multi_tool_agent/.env')
from agent import find_contracted_companies, check_public_trading_status

# Find contracted companies
result = find_contracted_companies('Oracle')
print(result['report'])

# Check trading status
result = check_public_trading_status('Oracle, Microsoft, Tesla')
print(result['report'])
"
```

## 🔧 Features

### 1. Find Contracted Companies
- Uses Gemini web search to find partners, suppliers, contractors
- Provides comprehensive business relationship information
- Real-time web search results

### 2. Check Public Trading Status
- Uses yfinance to verify if companies are publicly traded
- Returns stock symbols, exchanges, and official company names
- Handles both public and private companies

### 3. Legacy Functions
- Weather information (`get_weather`)
- Time information (`get_current_time`)

## 📊 Example Queries

- "Find Oracle's contracted companies that are publicly traded"
- "Which of Microsoft's partners can I invest in?"
- "Check if Accenture, Deloitte, PWC are publicly traded"
- "Show me Amazon's suppliers and their stock symbols"

## 🛠 Agent Details

- **Name**: contracted_companies_analyzer
- **Model**: gemini-2.0-flash
- **Functions**: 4 total (2 new + 2 legacy)

## 📝 Output Format

Both functions return structured dictionaries with:
- `status`: "success" or "error"
- `report`: Human-readable formatted report
- Additional metadata for programmatic use

## 🔑 Requirements

- Google API key (set in multi_tool_agent/.env)
- Virtual environment with google-genai and yfinance
- Internet connection for web search and stock data