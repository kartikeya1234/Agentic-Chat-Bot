from src.LanggraphAgenticAI.state.state import State


class BasicChatbotNode():
    """
    Basic ChatBot login implementation
    """
    def __init__(self, model) -> None:
        self.llm=model

    def process(self, state: State) -> dict:
        """
        Processes the input state and generates response        
        """
        return {"messages": self.llm.invoke(state['messages'])}