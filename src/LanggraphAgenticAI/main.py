import streamlit as st
from src.LanggraphAgenticAI.ui.streamlitui.loadui import LoadStreamlitUI
from src.LanggraphAgenticAI.LLMs.groq_llm import GroqLLM
from src.LanggraphAgenticAI.LLMs.openai_llm import OpenAILLM
from src.LanggraphAgenticAI.graph.graph_builder import GraphBuilder
from src.LanggraphAgenticAI.ui.streamlitui.display_result import DisplayResultStreamlit


def load_langgraph_agenticai_app():
    """Loads and runs the LangGraph AgenticAI application with Streamlit UI.
    """

    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI")

    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.timeframe
    else:
        user_message = st.chat_input("Enter your message:")

    if user_message:
        try:

            obj_llm_config = OpenAILLM(user_controls_input=user_input) if user_input.get('selected_llms') == 'OpenAI' \
                                else GroqLLM(user_controls_input=user_input)
            model = obj_llm_config.get_llm_model()

            if not model:
                st.error("Error: LLM model could not be initialized.")
                return

            usecase = user_input.get('selected_usecase')
            if not usecase:
                st.error("Error: No use case selected.")
                return

            graph_builder = GraphBuilder(model=model)
            try:
                graph = graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase=usecase, graph=graph, user_message=user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error: et up failed - {e}")
                return

        except Exception as e:
            raise ValueError(f"Error {e} has happened.")
            return
