import os
from tavily import TavilyClient
from dotenv import load_dotenv
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.parent.parent.parent
dotenv_path = project_root / '.env'
print(f"Loading .env from: {dotenv_path}")
load_dotenv(dotenv_path=dotenv_path)

def search(query: str):
    """
    Performs a search using the Tavily client.
    """
    tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
    response = tavily_client.search(query)
    return response
