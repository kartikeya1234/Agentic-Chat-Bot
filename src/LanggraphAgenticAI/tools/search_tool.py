from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode


def get_tools(**kwargs):
    """
    Return the list of tools to be used in the chatbot
    """ 
    tools = [TavilySearchResults(max_results=2)]
    return tools

def create_tool_node(tools):
    """Create and returns a tool node for the graph

    Args:
        tools (_type_): _description_
    """
    return ToolNode(tools=tools)