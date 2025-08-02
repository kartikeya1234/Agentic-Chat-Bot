from langgraph.graph import StateGraph, START, END
from src.LanggraphAgenticAI.state.state import State
from src.LanggraphAgenticAI.nodes.basic_chatbot_node import BasicChatbotNode
from src.LanggraphAgenticAI.nodes.chatbot_with_tool_node import ChatbotWithToolNode
from src.LanggraphAgenticAI.tools.search_tool import get_tools, create_tool_node
from src.LanggraphAgenticAI.nodes.ai_news_node import AINewsNode
from langgraph.prebuilt import tools_condition


class GraphBuilder:
    def __init__(self, model) -> None:
        self.llm = model
        self.graph_builder = StateGraph(State)

    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot using LangGraph.
        """
        self.basic_chatbot_node = BasicChatbotNode(model=self.llm)

        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def chatbot_with_web(self):
        """
        Builds a chatbot with web search ability.
        """
        tools = get_tools()
        tool_node = create_tool_node(tools=tools)

        llm = self.llm

        obj_chatbot_with_node = ChatbotWithToolNode(model=self.llm)
        chatbot_node = obj_chatbot_with_node.create_chatbot(tools=tools)

        self.graph_builder.add_node("chatbot", chatbot_node)
        self.graph_builder.add_node("tools", tool_node)

        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def ai_news_builder_graph(self):

         ai_news_node = AINewsNode(llm=self.llm)

         self.graph_builder.add_node("fetch_news", ai_news_node.fetch_news)
         self.graph_builder.add_node("summarize_news", ai_news_node.summarize_news)
         self.graph_builder.add_node("save_results", ai_news_node.save_results)

         self.graph_builder.set_entry_point("fetch_news")
         self.graph_builder.add_edge("fetch_news", "summarize_news")
         self.graph_builder.add_edge("summarize_news", "save_results")
         self.graph_builder.add_edge("save_results", END)

    def setup_graph(self, usecase:str, **kwargs):

        if usecase == 'Basic Chatbot':
            self.basic_chatbot_build_graph()
        elif usecase == 'Chatbot with Web':
            self.chatbot_with_web()
        elif usecase == 'AI News':
            self.ai_news_builder_graph()
        else:
            NotImplementedError


        return self.graph_builder.compile()
