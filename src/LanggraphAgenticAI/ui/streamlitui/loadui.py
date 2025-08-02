import streamlit as st
import os

from src.LanggraphAgenticAI.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self) -> None:
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        st.set_page_config(page_title=self.config.get_page_title(), layout="wide")
        st.header(self.config.get_page_title())
        st.session_state.timeframe = ''
        st.session_state.IsFetchButtonClicked = False

        with st.sidebar:
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            self.user_controls["selected_llms"] = st.selectbox("Select LLM", llm_options)

            if self.user_controls["selected_llms"] in ['Groq', "OpenAI"]:
                if self.user_controls["selected_llms"] == "Groq":
                    model_options = self.config.get_groq_model_options()
                    self.user_controls["selected_groq_model"] = st.selectbox("Select Model", model_options)
                    self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("Groq API Key", type="password")

                    if not self.user_controls["GROQ_API_KEY"]:
                        st.warning("Please enter you GROQ API key to proceed.")
                elif self.user_controls["selected_llms"] == "OpenAI":
                    model_options = self.config.get_openai_model_options()
                    self.user_controls["selected_openai_model"] = st.selectbox("Select Model", model_options)
                    self.user_controls["OPENAI_API_KEY"] = st.session_state["OPENAI_API_KEY"] = st.text_input("OpenAI API Key", type="password")

                    if not self.user_controls["OPENAI_API_KEY"]:
                        st.warning("Please enter you OPENAI API key to proceed.")

            self.user_controls["selected_usecase"] = st.selectbox("Select Usecases", usecase_options)
            if self.user_controls["selected_usecase"] in ['Chatbot with Web', 'AI News']:
                os.environ['TAVILY_API_KEY'] = self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = st.text_input("Tavily API Key", type="password")

                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("Please enter your Tavily API key to proceed.")

                if self.user_controls["selected_usecase"] == 'AI News':
                    st.subheader("AI News Explorer")

                    with st.sidebar:
                        time_frame = st.selectbox(
                            "Select Time Frame",
                            ["Daily", "Weekly", "Monthly"],
                            index=0
                        )
                    if st.button("Fetch Latest AI News", use_container_width=True):
                        st.session_state.IsFetchButtonClicked = True
                        st.session_state.timeframe = time_frame


        return self.user_controls
