#!/usr/bin/env python3.13
"""
Demo of the Contracted Companies Analyzer Agent
"""

import os
import sys

# Add the virtual environment to path
sys.path.insert(0, '.venv_current/lib/python3.13/site-packages')
sys.path.insert(0, 'multi_tool_agent')

from dotenv import load_dotenv
load_dotenv('multi_tool_agent/.env')

from agent import root_agent, find_contracted_companies, check_public_trading_status

def main():
    print("🚀 Contracted Companies Analyzer Agent - DEMO")
    print("=" * 60)
    print(f"Agent: {root_agent.name}")
    print(f"Description: {root_agent.description}")
    print("\nAvailable Functions:")
    for i, tool in enumerate(root_agent.tools, 1):
        print(f"{i}. {tool.__name__}")
    print("\n" + "=" * 60)

    # Demo 1: Check trading status
    print("\n📊 DEMO 1: Checking Trading Status")
    print("-" * 40)
    companies_to_check = "Oracle, Microsoft, Tesla, PWC, Apple"
    print(f"Checking: {companies_to_check}")

    result = check_public_trading_status(companies_to_check)
    if result['status'] == 'success':
        print(result['report'])
        print(f"Summary: {result['public_count']} public, {result['private_count']} private companies")
    else:
        print(f"Error: {result['error_message']}")

    print("\n" + "=" * 60)
    print("🎯 DEMO 2: Finding Contracted Companies (Web Search)")
    print("-" * 40)
    print("Searching for Oracle's contracted companies...")

    result = find_contracted_companies("Oracle")
    if result['status'] == 'success':
        # Show first 500 characters of the report
        report = result['report']
        if len(report) > 500:
            print(report[:500] + "...\n[Report truncated for demo]")
        else:
            print(report)
    else:
        print(f"Error: {result['error_message']}")

    print("\n" + "=" * 60)
    print("✅ Demo completed! Agent is ready for interactive use.")
    print("\nTo run interactively: ./.venv_current/bin/python3.13 run_agent.py")

if __name__ == "__main__":
    main()