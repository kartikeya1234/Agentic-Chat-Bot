import streamlit as st
import os
from langchain_openai import ChatOpenAI

class OpenAILLM:
    def __init__(self, user_controls_input) -> None:
        self.user_controls_input = user_controls_input

    def get_llm_model(self):
        try: 
            openai_api_key = self.user_controls_input["OPENAI_API_KEY"]
            selected_openai_model = self.user_controls_input["selected_openai_model"]

            if openai_api_key == '' and os.environ["OPENAI_API_KEY"] == '':
                st.error("Please enter the Groq API KEY")
            
            llm = ChatOpenAI(api_key=openai_api_key, model=selected_openai_model)

        except Exception as e:
            raise ValueError(f"Error occured with exception: {e}")
        return llm