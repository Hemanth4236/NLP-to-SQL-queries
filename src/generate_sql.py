from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_sql(question):

    schema = """
    Table: employees
    Columns:
    emp_id, name, department, salary
    """

    prompt = f"""
    Convert the natural language question into SQL.

    Schema:
    {schema}

    Question:
    {question}

    Return only the SQL query.
    """

    response = client.responses.create(
        model="gpt-4.1",
        input=prompt
    )

    return response.output_text