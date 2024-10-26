import os
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from crewai import LLM
from dotenv import load_dotenv
from src.llm_factory.llm_types import get_model_by_quality

# Load environment variables
load_dotenv()

# Environment variables
modal_name = "gpt-4"
api_key = os.getenv("OPENAI_API_KEY")
endpoint = os.getenv("LANGCHAIN_ENDPOINT")
project = os.getenv("LANGCHAIN_PROJECT")
api_grog_key = os.getenv("GROQ_API_KEY")
acidaes_llm_url = os.getenv("URL_LLAMA")

def get_llm_base_model(index): 
    modal_name = get_model_by_quality(index)
    print("Modal Name", modal_name)
    return ChatGroq(
        model=modal_name,
        temperature=0.0,
        max_retries=2,
        api_key=api_grog_key
        # other params...
    )

def get_grog_llm_with_tools(index, tools):
    llm = get_llm_base_model(index)
    if tools is None:
        ValueError("you must be pass tool")
    return llm.bind_tools(tools)

def get_openai_base_llm():
    return ChatOpenAI(
        model="gpt-3.5-turbo", 
        api_key=api_key,
        temperature=0,
        verbose=True,
        max_retries=2
    )

def get_openai_llm():
    return get_openai_base_llm()

def get_openai_llm_with_tools(tools):
    llm = get_openai_base_llm()
    if tools is None:
        ValueError("you must be pass tool")
    return llm.bind_tools(tools)


def get_acidaes_base_llm():
    return ChatOpenAI(
        model='qwen2', 
        api_key="local",
        base_url='http://192.168.0.164:11434/v1',
        temperature=0,
        verbose=True
    )

def get_acidaes_llm(tools):
    llm =  get_acidaes_base_llm()
    
    return llm.bind_tools(tools)

def get_po_llm():
    return LLM(
    model='gpt-3.5-turbo',
    api_key=api_key
)

def get_acidaes_llm_for_crew():
    return LLM(
    model='qwen2',
    provider='custom',
    base_url='http://192.168.0.164:11434/v1',
    api_key="local"
    )
    
def get_grog_llm_for_crew(index):
     modal_name = get_model_by_quality(index)
     return LLM(
        model="llama3-8b-8192",
        provider="custom",
        base_url="https://api.modelservice.com/v1",
        api_key=api_grog_key
        )
     
def get_acidaes_llama_llm():
   return ChatOpenAI(
        model='llama3.2', 
        api_key="local",
        base_url='http://192.168.0.163:11435/v1',
        temperature=0,
        verbose=True
    )
def get_acidaes_llama_llm_with_tools(tools):
    llm =  get_acidaes_llama_llm()
    
    return llm.bind_tools(tools)

def get_acidaes_llama_llm_crew():
   return LLM(
        model='llama3.2', 
        api_key="local",
        base_url='http://192.168.0.163:11435/v1',
        temperature=0,
        verbose=True
    )