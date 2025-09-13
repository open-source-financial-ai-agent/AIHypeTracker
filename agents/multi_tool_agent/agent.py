import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google import genai
from google.genai import types
import yfinance as yf
import os
from typing import List, Dict

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


root_agent = Agent(
    name="contracted_companies_analyzer",
    model="gemini-2.0-flash",
    description=(
        "Agent to find contracted companies for big tech companies and analyze their public trading status for investment opportunities."
    ),
    instruction=(
        "You are a helpful agent who can find contracted companies, partners, and suppliers for major tech companies "
        "and determine which ones are publicly traded. This helps users identify potential investment opportunities "
        "based on corporate relationships. You can also provide weather and time information when needed."
    ),
    tools=[find_contracted_companies, check_public_trading_status, get_weather, get_current_time],
)