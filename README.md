# Product Demo
<img width="1355" height="954" alt="image" src="https://github.com/user-attachments/assets/2082f9a6-217e-4a25-a0de-cd6f50b3cac2" />


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

## 🌐 **Web Frontend Interface**

We've built a beautiful web frontend that provides an intuitive interface for investment analysis:

### **Features:**
- 🔍 **Smart Company Search** - Enter any company name to discover investment opportunities
- 📈 **Real-time Data Visualization** - Interactive charts showing profit margins and financial metrics
- 💼 **Comprehensive Analysis** - Displays contracted companies with their financial data
- 📱 **Responsive Design** - Works perfectly on desktop and mobile devices
- ⚡ **Fast Performance** - Real-time API integration with our financial analysis agent

### **How to Use the Frontend:**

```bash
# Start the web frontend
./.venv_current/bin/python3.13 start_frontend.py
```

Then open your browser to: **http://localhost:8002**

### **What You'll See:**
1. **Search Interface** - Enter a company name (e.g., "Oracle", "Microsoft")
2. **Analysis Results** - View contracted companies and their financial metrics
3. **Data Visualizations** - Interactive charts showing:
   - Profit margins (Gross, Operating, Net)
   - Market capitalization comparisons
   - Revenue and financial health indicators
4. **Investment Insights** - Comprehensive JSON data for each publicly traded partner

### **Example Search Results:**
- Input: "Oracle"
- Output: Financial data for Accenture, Microsoft, Intel, and other Oracle partners
- Visualizations: Profit margin charts, market cap comparisons, financial health scores

## 🔑 Requirements

- Google API key (set in multi_tool_agent/.env)
- Virtual environment with google-genai and yfinance
- Internet connection for web search and stock data
