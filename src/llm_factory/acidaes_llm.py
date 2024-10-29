import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_experimental.llms.ollama_functions import OllamaFunctions

load_dotenv()


class llm_next:
    def __init__(self):
        self.openai_model = "gpt-3.5-turbo"
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_uri = os.getenv("ACID_API_KEY")
        self.project = os.getenv("LANGCHAIN_ENDPOINT")
        self.endpoint = os.getenv("LANGCHAIN_PROJECT")

    def get_open_ai_llm(self):
        return ChatOpenAI(
            model=self.openai_model, api_key=self.api_key, temperature=0.5, verbose=True
        )

    def get_open_ai_llm_with_tools(self, tools=None):
        llm = self.get_open_ai_llm()
        if tools is None:
            raise ValueError("You must pass tools")

        return llm.bind_tools(tools)

    def get_acidaes_llm(self):
        return ChatOpenAI(
            model="llama3.2",
            api_key="local",
            base_url=self.base_uri,
            temperature=0,
            verbose=True,
        )

    def get_acidaes_llm_with_tool(self, tools=None):
        llm = self.get_acidaes_llm()
        if tools is None:
            raise ValueError("You must pass tools")

        return llm.bind_tools(tools)

    def get_ollama_llm(self):
        return OllamaFunctions(
            model="llama3.2",
            api_key="local",
            base_url=self.base_uri,
            temperature=0,
            verbose=True
        )
        


# Usage
next_llm = llm_next()
