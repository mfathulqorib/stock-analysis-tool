import os

from tavily import TavilyClient

TAVILY_API_KEY = os.environ["TAVILY_API_KEY"]
if not TAVILY_API_KEY:
    raise EnvironmentError("TAVILY_API_KEY must be set in env!")

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
