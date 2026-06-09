import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

print("API KEY FOUND: ", bool(api_key))


llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    model="deepseek/deepseek-chat-v3-0324"
)

print(os.getenv("OPENROUTER_API_KEY"))