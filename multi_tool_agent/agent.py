import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google import genai
from google.genai import types
import yfinance as yf
import os
import json
from typing import List, Dict, Optional, Union

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}


def find_contracted_companies(company_name: str) -> dict:
    """Finds contracted companies, partners, and suppliers for a given tech company using Gemini web search.

    Args:
        company_name (str): The name of the tech company to search for (e.g., "Oracle", "Microsoft").

    Returns:
        dict: status and result or error msg with list of contracted companies found.
    """
    try:
        # Set up Gemini client with API key from environment
        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

        # Define the grounding tool for web search
        grounding_tool = types.Tool(google_search=types.GoogleSearch())

        # Configure generation settings
        config = types.GenerateContentConfig(tools=[grounding_tool])

        # Create search query
        search_prompt = (
            f"Find the major contracted companies, business partners, suppliers, and vendors "
            f"that work with {company_name}. List the company names clearly and focus on "
            f"significant business relationships and partnerships. Include companies that "
            f"provide services or products to {company_name} or have major contracts with them."
        )

        # Make the request with web search
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=search_prompt,
            config=config,
        )

        return {
            "status": "success",
            "report": f"Contracted companies for {company_name}:\n{response.text}",
            "company_searched": company_name
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Unable to search for contracted companies for '{company_name}': {str(e)}"
        }


def check_public_trading_status(company_names: str) -> dict:
    """Checks if companies are publicly traded using yfinance.

    Args:
        company_names (str): Comma-separated list of company names to check.

    Returns:
        dict: status and result with trading status for each company.
    """
    try:
        companies = [name.strip() for name in company_names.split(",")]
        results = []

        for company in companies:
            if not company:
                continue

            # Common stock symbols for well-known companies
            symbol_mappings = {
                "oracle": "ORCL",
                "microsoft": "MSFT",
                "apple": "AAPL",
                "google": "GOOGL",
                "alphabet": "GOOGL",
                "amazon": "AMZN",
                "meta": "META",
                "facebook": "META",
                "nvidia": "NVDA",
                "tesla": "TSLA",
                "salesforce": "CRM",
                "servicenow": "NOW",
                "workday": "WDAY",
                "adobe": "ADBE",
                "intel": "INTC",
                "ibm": "IBM",
                "sap": "SAP",
                "accenture": "ACN",
                "deloitte": "DLX",  # Deloitte Tax LLP
                "pwc": None,  # Private
                "kpmg": None,  # Private
                "ey": None,  # Private
            }

            # Try to find a symbol for the company
            company_lower = company.lower()
            symbol = symbol_mappings.get(company_lower)

            if symbol is None:
                # For companies we know are private
                if company_lower in ["pwc", "kpmg", "ey", "ernst & young"]:
                    results.append({
                        "company": company,
                        "is_public": False,
                        "symbol": None,
                        "status": "Known private company"
                    })
                    continue
                else:
                    # Try common symbol patterns
                    possible_symbols = [
                        company.upper()[:4],  # First 4 letters
                        company.upper()[:3],  # First 3 letters
                        company.replace(" ", "").upper()[:4]  # Remove spaces, first 4 letters
                    ]

                    found = False
                    for test_symbol in possible_symbols:
                        try:
                            ticker = yf.Ticker(test_symbol)
                            info = ticker.info
                            if info and 'symbol' in info:
                                symbol = test_symbol
                                found = True
                                break
                        except:
                            continue

                    if not found:
                        results.append({
                            "company": company,
                            "is_public": False,
                            "symbol": None,
                            "status": "No public trading symbol found"
                        })
                        continue

            # Check if the symbol is valid and get company info
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info

                if info and len(info) > 1:  # yfinance returns minimal dict if symbol doesn't exist
                    company_name = info.get('longName', info.get('shortName', company))
                    exchange = info.get('exchange', 'Unknown')

                    results.append({
                        "company": company,
                        "is_public": True,
                        "symbol": symbol,
                        "official_name": company_name,
                        "exchange": exchange,
                        "status": "Publicly traded"
                    })
                else:
                    results.append({
                        "company": company,
                        "is_public": False,
                        "symbol": None,
                        "status": "Symbol exists but no trading data found"
                    })

            except Exception as e:
                results.append({
                    "company": company,
                    "is_public": False,
                    "symbol": symbol,
                    "status": f"Error checking symbol {symbol}: {str(e)}"
                })

        # Format the results
        public_companies = [r for r in results if r["is_public"]]
        private_companies = [r for r in results if not r["is_public"]]

        report = f"Trading Status Analysis:\n\n"

        if public_companies:
            report += "📈 PUBLICLY TRADED COMPANIES:\n"
            for company in public_companies:
                report += f"• {company['company']} ({company['symbol']}) - {company['official_name']} on {company['exchange']}\n"
            report += "\n"

        if private_companies:
            report += "🔒 NON-PUBLIC/PRIVATE COMPANIES:\n"
            for company in private_companies:
                report += f"• {company['company']} - {company['status']}\n"

        return {
            "status": "success",
            "report": report,
            "detailed_results": results,
            "public_count": len(public_companies),
            "private_count": len(private_companies)
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Unable to check trading status: {str(e)}"
        }


def get_company_financial_metrics(stock_ticker: str) -> dict:
    """Gets key financial metrics for a company from its stock ticker and calculates profit margins.

    Args:
        stock_ticker (str): The stock ticker symbol (e.g., "ORCL", "MSFT", "AAPL").

    Returns:
        dict: JSON-formatted financial metrics including calculated margins.
    """
    try:
        ticker = yf.Ticker(stock_ticker.upper())

        # Get company info for basic data
        info = ticker.info

        # Get financial statements (income statement)
        financials = ticker.financials

        if financials.empty or not info:
            return {
                "status": "error",
                "error_message": f"No financial data found for ticker '{stock_ticker}'. Please verify the ticker symbol is correct."
            }

        # Get the most recent year of financial data
        latest_year = financials.columns[0]

        # Helper function to safely get financial data
        def safe_get_financial(metric_name: str, source: str = 'financials') -> Optional[float]:
            try:
                if source == 'financials':
                    if metric_name in financials.index:
                        value = financials.loc[metric_name, latest_year]
                        return float(value) if value and str(value) != 'nan' else None
                elif source == 'info':
                    return info.get(metric_name)
                return None
            except:
                return None

        # Extract key financial metrics
        metrics = {
            # Company Information
            "company_name": info.get('longName', info.get('shortName', stock_ticker)),
            "ticker": stock_ticker.upper(),
            "currency": info.get('currency', 'USD'),
            "fiscal_year_end": str(latest_year.date()) if latest_year else None,

            # Market Metrics
            "market_cap": info.get('marketCap'),
            "enterprise_value": info.get('enterpriseValue'),

            # Revenue Metrics
            "annual_revenue": safe_get_financial('Total Revenue') or info.get('totalRevenue'),
            "cost_of_goods_sold": safe_get_financial('Cost Of Revenue'),

            # Profitability Metrics
            "gross_profit": safe_get_financial('Gross Profit'),
            "operating_income": safe_get_financial('Operating Income'),
            "net_income": safe_get_financial('Net Income'),

            # Interest Metrics
            "interest_income": safe_get_financial('Interest Income'),
            "interest_expense": safe_get_financial('Interest Expense'),
            "net_interest_income": safe_get_financial('Net Interest Income'),

            # Other Key Metrics
            "total_expenses": safe_get_financial('Total Expenses'),
            "operating_expenses": safe_get_financial('Operating Expense'),
            "ebitda": safe_get_financial('EBITDA'),
            "ebit": safe_get_financial('EBIT'),
        }

        # Calculate profit margins
        annual_revenue = metrics["annual_revenue"]
        calculated_margins = {}

        if annual_revenue and annual_revenue > 0:
            # Gross Profit Margin = (Gross Profit / Annual Revenue) * 100
            if metrics["gross_profit"]:
                calculated_margins["gross_profit_margin_percent"] = round(
                    (metrics["gross_profit"] / annual_revenue) * 100, 2
                )

            # Operating Profit Margin = (Operating Income / Annual Revenue) * 100
            if metrics["operating_income"]:
                calculated_margins["operating_profit_margin_percent"] = round(
                    (metrics["operating_income"] / annual_revenue) * 100, 2
                )

            # Net Profit Margin = (Net Income / Annual Revenue) * 100
            if metrics["net_income"]:
                calculated_margins["net_profit_margin_percent"] = round(
                    (metrics["net_income"] / annual_revenue) * 100, 2
                )

            # EBITDA Margin = (EBITDA / Annual Revenue) * 100
            if metrics["ebitda"]:
                calculated_margins["ebitda_margin_percent"] = round(
                    (metrics["ebitda"] / annual_revenue) * 100, 2
                )

        # Add pre-calculated margins from yfinance info if available
        yfinance_margins = {
            "yf_gross_margin_percent": round(info.get('grossMargins', 0) * 100, 2) if info.get('grossMargins') else None,
            "yf_operating_margin_percent": round(info.get('operatingMargins', 0) * 100, 2) if info.get('operatingMargins') else None,
            "yf_profit_margin_percent": round(info.get('profitMargins', 0) * 100, 2) if info.get('profitMargins') else None,
        }

        # Combine all data
        financial_data = {
            **metrics,
            **calculated_margins,
            **yfinance_margins
        }

        # Format large numbers for display
        def format_currency(value: Optional[float]) -> str:
            if value is None:
                return "N/A"
            if abs(value) >= 1e12:
                return f"${value/1e12:.2f}T"
            elif abs(value) >= 1e9:
                return f"${value/1e9:.2f}B"
            elif abs(value) >= 1e6:
                return f"${value/1e6:.2f}M"
            elif abs(value) >= 1e3:
                return f"${value/1e3:.2f}K"
            else:
                return f"${value:,.2f}"

        # Create formatted summary
        summary = {
            "company": financial_data["company_name"],
            "ticker": financial_data["ticker"],
            "market_cap": format_currency(financial_data["market_cap"]),
            "annual_revenue": format_currency(financial_data["annual_revenue"]),
            "gross_profit": format_currency(financial_data["gross_profit"]),
            "operating_income": format_currency(financial_data["operating_income"]),
            "net_income": format_currency(financial_data["net_income"]),
            "gross_margin": f"{financial_data.get('gross_profit_margin_percent', 'N/A')}%" if financial_data.get('gross_profit_margin_percent') else "N/A",
            "operating_margin": f"{financial_data.get('operating_profit_margin_percent', 'N/A')}%" if financial_data.get('operating_profit_margin_percent') else "N/A",
            "net_margin": f"{financial_data.get('net_profit_margin_percent', 'N/A')}%" if financial_data.get('net_profit_margin_percent') else "N/A"
        }

        return {
            "status": "success",
            "summary": summary,
            "detailed_metrics": financial_data,
            "json_data": json.dumps(financial_data, indent=2, default=str),
            "fiscal_year": str(latest_year.date()) if latest_year else "Unknown"
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Unable to retrieve financial data for '{stock_ticker}': {str(e)}"
        }


root_agent = Agent(
    name="financial_investment_analyzer",
    model="gemini-2.0-flash",
    description=(
        "Comprehensive financial analysis agent that finds contracted companies, analyzes public trading status, "
        "and provides detailed financial metrics with profit margins for investment decision-making."
    ),
    instruction=(
        "You are a comprehensive financial analysis agent with the following capabilities:\n"
        "1. Find contracted companies, partners, and suppliers for major tech companies using web search\n"
        "2. Determine which companies are publicly traded and provide stock symbols\n"
        "3. Get detailed financial metrics including market cap, revenue, profit margins, and key ratios\n"
        "4. Calculate and analyze profit margins (gross, operating, net) for investment analysis\n"
        "5. Provide weather and time information when needed\n\n"
        "Use these tools to help users identify investment opportunities based on corporate relationships "
        "and comprehensive financial analysis."
    ),
    tools=[find_contracted_companies, check_public_trading_status, get_company_financial_metrics, get_weather, get_current_time],
)