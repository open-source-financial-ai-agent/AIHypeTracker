#!/usr/bin/env python3.13
"""
Demo of the new Financial Metrics function
"""

import sys
import os

# Add the virtual environment to path
sys.path.insert(0, '.venv_current/lib/python3.13/site-packages')
sys.path.insert(0, 'multi_tool_agent')

from dotenv import load_dotenv
load_dotenv('multi_tool_agent/.env')

from agent import get_company_financial_metrics

def main():
    print("📊 Financial Metrics Analyzer - DEMO")
    print("=" * 60)

    # Demo companies
    companies = ["ORCL", "MSFT", "AAPL", "GOOGL", "TSLA"]

    for i, ticker in enumerate(companies, 1):
        print(f"\n{i}. Analyzing {ticker}:")
        print("-" * 40)

        result = get_company_financial_metrics(ticker)

        if result['status'] == 'success':
            summary = result['summary']
            print(f"Company: {summary['company']}")
            print(f"Market Cap: {summary['market_cap']}")
            print(f"Annual Revenue: {summary['annual_revenue']}")
            print(f"Gross Profit: {summary['gross_profit']}")
            print(f"Operating Income: {summary['operating_income']}")
            print()
            print("📈 Profit Margins:")
            print(f"  Gross Margin: {summary['gross_margin']}")
            print(f"  Operating Margin: {summary['operating_margin']}")
            print(f"  Net Margin: {summary['net_margin']}")

            # Show JSON structure exists
            print(f"\n✅ Full JSON data available ({len(result['json_data'])} characters)")
            print(f"📅 Fiscal Year: {result['fiscal_year']}")
        else:
            print(f"❌ Error: {result['error_message']}")

        if i < len(companies):
            print("\n" + "=" * 60)

    print("\n" + "=" * 60)
    print("✅ Demo completed!")
    print("\n🔧 Available Usage Methods:")
    print("1. CLI: ./.venv_current/bin/python3.13 run_agent.py")
    print("2. Web: ./.venv_current/bin/adk web agents --port 8080")
    print("3. Demo: ./.venv_current/bin/python3.13 demo.py")

if __name__ == "__main__":
    main()