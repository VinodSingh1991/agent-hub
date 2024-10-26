import os

from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv

modal_name = "gpt-4"
apiKey = os.getenv("OPENAI_API_KEY")
end_point = os.getenv("LANGCHAIN_ENDPOINT")
project = os.getenv("LANGCHAIN_PROJECT")
temperature = 0.5
api_grog_key = os.getenv("GROQ_API_KEY")
acidaes_llm_url = os.getenv("URL_LLAMA")


load_dotenv()

# Ensure API key is set
if not apiKey:
    print("OPENAI_API_KEY is", apiKey)
    raise ValueError("API_KEY is not set", )

# Initialize the OpenAI chat model (Check if endpoint/project is needed for your use case)
llm = ChatOpenAI(
    model=modal_name, 
    api_key=apiKey,
    temperature=temperature,
    verbose=True
)

def get_llm():
    return llm

def get_llm_modal_with_tools(tools):
    if tools is None:
        ValueError("you must be pass tool")
    
    return llm.bind_tools(tools)




def get_grog_llm(tools):
    llm = ChatGroq(
        model="llama3-8b-8192",
        temperature=0.0,
        max_retries=2,
        api_key=api_grog_key,
        # other params...
    )
    
    if tools is None:
        ValueError("you must be pass tool")
        
    return llm.bind_tools(tools)

def acidaes_llm(tools):
    llm = ChatOpenAI(
        model='qwen2', 
        api_key="local",
        temperature=temperature,
        verbose=True,
        base_url= acidaes_llm_url
        # Uncomment these if you are indeed using them
        # endpoint=end_point,
        # project=project
    )

    if tools is None:
        ValueError("you must be pass tool")
        
    return llm.bind_tools(tools)

def get_llm_mixtral(tools):
    llm =  ChatOpenAI(
        model="qwen2",
        base_url="http://192.168.0.164:11434/v1"
    )
    
    if tools is None:
        ValueError("you must be pass tool")
        
    return llm.bind_tools(tools)