#!/usr/bin/env python3.13
"""
Contracted Companies Analyzer Agent Runner
"""

import os
import sys

# Add the virtual environment to path
sys.path.insert(0, '.venv_current/lib/python3.13/site-packages')

# Add multi_tool_agent to path
sys.path.insert(0, 'multi_tool_agent')

from dotenv import load_dotenv
load_dotenv('multi_tool_agent/.env')

from agent import root_agent, find_contracted_companies, check_public_trading_status

def main():
    print("🚀 Contracted Companies Analyzer Agent")
    print("=" * 50)
    print(f"Agent: {root_agent.name}")
    print(f"Description: {root_agent.description}")
    print("\nAvailable Functions:")
    for i, tool in enumerate(root_agent.tools, 1):
        print(f"{i}. {tool.__name__}")
    print("\n" + "=" * 50)

    while True:
        print("\nChoose an option:")
        print("1. Find contracted companies")
        print("2. Check public trading status")
        print("3. Exit")

        choice = input("\nEnter choice (1-3): ").strip()

        if choice == "1":
            company = input("Enter company name (e.g., Oracle, Microsoft): ").strip()
            if company:
                print(f"\n🔍 Searching for contracted companies of {company}...")
                result = find_contracted_companies(company)
                if result['status'] == 'success':
                    print(result['report'])
                else:
                    print(f"Error: {result['error_message']}")

        elif choice == "2":
            companies = input("Enter comma-separated company names: ").strip()
            if companies:
                print(f"\n📊 Checking trading status...")
                result = check_public_trading_status(companies)
                if result['status'] == 'success':
                    print(result['report'])
                else:
                    print(f"Error: {result['error_message']}")

        elif choice == "3":
            print("Goodbye! 👋")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()