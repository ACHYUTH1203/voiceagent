import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()


if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found. Please check your .env file.")


llm = ChatOpenAI(
    model="gpt-4o-mini",  # Corrected model name
    temperature=0
)


def generate_llm_response(prompt: str) -> str:
    response = llm.invoke(prompt)
    return response.content

