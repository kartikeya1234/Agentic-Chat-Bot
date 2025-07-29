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
    
        with st.sidebar:
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            self.user_controls["selected_llms"] = st.selectbox("Select LLM", llm_options)

            if self.user_controls["selected_llms"] in ['Groq', "OpenAI"]:
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_models"] = st.selectbox("Select Model", model_options)
                if self.user_controls["selected_llms"] == "Groq":
                    self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("Groq API Key", type="password")

                    if not self.user_controls["GROQ_API_KEY"]:
                        st.warning("Please enter you GROQ API key to proceed.")

            self.user_controls["selected_usecase"] = st.selectbox("Select Usecases", usecase_options)

        return self.user_controls

