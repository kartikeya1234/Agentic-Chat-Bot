from src.LanggraphAgenticAI.state.state import State


class ChatbotWithToolNode:
    """
    Chatbot with tools integeration
    """
    def __init__(self, model) -> None:
        self.llm = model

    def process(self, state:State):
        """_summary_

        Args:
            state (State): _description_
        """
        user_input = state["messages"][-1] if state["messages"] else ""
        llm_response = self.llm.invoke([{"role": "user", "content": user_input}])

        tools_response = f"Tool integration for: {user_input}"

        return {"messages": [llm_response, tools_response]}
    
    def create_chatbot(self, tools):
        """_summary_

        Args:
            tools (_type_): _description_
        """
        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State):
            """Chatbot logic for processing the input state and returning a response

            Args:
                state (State): _description_
            """
            return {"messages": [llm_with_tools.invoke(state["messages"])]}
        
        return chatbot_node