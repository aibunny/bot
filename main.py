# main.py
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.llms.openai import OpenAI
from langchain.sql_database import SQLDatabase


from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")


class Message(BaseModel):
    content: str


DATABASE_URL = os.getenv('DATABASE_URL')

db = SQLDatabase.from_uri(DATABASE_URL)

toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0))

# callback=FinalStreamingStdOutCallbackHandler()

agent_executor = create_sql_agent(
    llm=OpenAI(
        streaming=True,
        temperature=0
    ),
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)



@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/stream_chat/")
async def stream_chat(message: Message):
    result = agent_executor.run(message.content)
    return result
