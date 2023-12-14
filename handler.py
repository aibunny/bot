import os
from dotenv import load_dotenv
from langchain_experimental.sql import SQLDatabaseSequentialChain
from langchain.utilities import SQLDatabase
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate

load_dotenv()


DATABASE_URL = os.getenv('DATABASE_URL')

db = SQLDatabase.from_uri(DATABASE_URL)

llm = HuggingFaceHub(
        repo_id="HuggingFaceH4/zephyr-7b-beta",
        model_kwargs={"max_length": 512}
        )

#question =" list top 5 customers along with their total orders in table format"

def execute_prompt(question):
    PROMPT = """ 
    Given an input question, first create a syntactically correct SQL query to run,  
    then look at the results of the query and return the answer in markdown format.If user requests explicitly requires
    data in table format generate a markdown table with the data.
    If the question is not related to anything in the database respond with:"NOT RELATED"  
    The question: {question}
    """

    db_chain = SQLDatabaseSequentialChain.from_llm(llm,db)

    result = db_chain.run(PROMPT.format(question=question))
    print(result)
    return result

result = execute_prompt("list top 5 customers along with their total orders in table format")
print(result)