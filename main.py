from fastapi import FastAPI
#from src.sales_assistant.lead_api import start_app
#from src.po_assistant.main import pag_crew_result
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
#from src.po_assistant.main import start_po_app
#from src.sales_assistant.app import start_sales_app
#from src.po_assistant.crew import po_start_app
#from src.coding_agent.app import run_coding_agent
#from langgraph.graph.message import AnyMessage, add_messages
from src.service_assistant.app import start_service_app
from src.service_assistant.get_accounts import get_accounts_list

app = FastAPI()

origins = ["http://127.0.0.1:5173", "http://localhost:5003", "http://127.0.0.1:5173"]

# Define the request body
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


class Imessage(BaseModel):
    message: str


# # Allow requests from your React app (adjust this if your frontend runs elsewhere)
# @app.post("/api/sales_agent")
# async def root(message: Imessage):
#     return start_sales_app(message.message)


# @app.post("/api/po_agent")
# async def root(message: Imessage):
#     return po_start_app(message.message)

# @app.post("/api/coding_agent")
# async def run_coding_agent_root(message: Imessage):
#     return run_coding_agent(message.message)

# @app.post("/api/po_assitant")
# async def root(message: Imessage):
#     return start_po_app(message)

# Allow requests from your React app (adjust this if your frontend runs elsewhere)
@app.post("/api/service_agent")
async def root():
    return start_service_app()

@app.get("/api/accounts")
async def root():
    return get_accounts_list()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="localhost", port=8000)
