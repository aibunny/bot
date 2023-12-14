import os
from dotenv import load_dotenv
from langchain_experimental.sql import SQLDatabaseSequentialChain
from langchain.utilities import SQLDatabase
from langchain.llms import HuggingFaceHub, OpenAI
from langchain.prompts import PromptTemplate

load_dotenv()

DEBUG = os.getenv('DEBUG', False)

DATABASE_URL = os.getenv('DATABASE_URL')

db = SQLDatabase.from_uri(DATABASE_URL)

def get_llm():
    if DEBUG:
        llm = HuggingFaceHub(
        repo_id="HuggingFaceH4/zephyr-7b-beta",
        model_kwargs={"max_length": 512}
        )
    else:
        llm=OpenAI(
        streaming=True,
        temperature=0
        )
    return llm
        


def execute_prompt(question):
    PROMPT = """ 
    Given an input question, first create a syntactically correct SQL query to run, 
    Ensure the SQL query is correct and it matches the table names to avoid any errors before running. 
    then look at the results of the query and return the answer in markdown format.If user requests explicitly requires
    data in table format generate a markdown table with the data.   
    
    The question: {question}
    """

    db_chain = SQLDatabaseSequentialChain.from_llm(get_llm(),db)

    result = db_chain.run(PROMPT.format(question=question))
    print(result)
    return result

