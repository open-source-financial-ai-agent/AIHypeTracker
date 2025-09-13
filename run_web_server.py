#!/usr/bin/env python3.13
"""
Start the Google ADK web server for the Contracted Companies Analyzer Agent
"""

import sys
import os

# Add the virtual environment to path
sys.path.insert(0, '.venv_current/lib/python3.13/site-packages')
sys.path.insert(0, 'multi_tool_agent')

from dotenv import load_dotenv
load_dotenv('multi_tool_agent/.env')

from google.adk.apps import App
from google.adk.runners import Runner, InMemorySessionService, InMemoryArtifactService, InMemoryMemoryService
from agent import root_agent

def main():
    print("🚀 Starting Google ADK Web Server...")
    print("=" * 50)

    try:
        # Create the ADK App
        print(f"Creating app with agent: {root_agent.name}")
        app = App(
            name="Contracted Companies Analyzer",
            root_agent=root_agent
        )

        print("✅ App created successfully!")

        # Create the required services
        print("Creating services...")
        session_service = InMemorySessionService()
        artifact_service = InMemoryArtifactService()
        memory_service = InMemoryMemoryService()

        # Create the runner with all required services
        print("Creating runner...")
        runner = Runner(
            app=app,
            session_service=session_service,
            artifact_service=artifact_service,
            memory_service=memory_service
        )

        print("✅ Runner created successfully!")
        print("=" * 50)

        # Start the server
        print("🌐 Starting web server...")
        print("The server should be available at: http://localhost:8080")
        print("Press Ctrl+C to stop the server")
        print("=" * 50)

        # This will start the web server
        runner.run()

    except KeyboardInterrupt:
        print("\n👋 Shutting down server...")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()