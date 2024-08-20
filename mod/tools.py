from langchain_community.tools.tavily_search import TavilySearchResults

tavily_tool = [TavilySearchResults(max_results=1)]

dispatcher_tools = []
