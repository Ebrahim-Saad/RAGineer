from src.core import config

from langchain_tavily import TavilySearchResults
from langchain_core.tools import tool

keys = config.get_keys()


@tool
def internt_search(query: str) -> str:
    """Search the internet for information"""
    search = TavilySearchResults(api_key=keys.TAVILY_API_KEY)
    return search.run(query)

@tool
def ask_user(query: str) -> str:
    """Ask the user about something"""
    return input(query)



def get_tools() -> list[BaseTool]:
    return [internt_search, ask_user]