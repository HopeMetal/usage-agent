import os
import dotenv

dotenv.load_dotenv()

from langchain_openai import AzureChatOpenAI

def model_init(deployment= "gpt-4o") -> AzureChatOpenAI:
    return AzureChatOpenAI(
        azure_endpoint=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY"),
        api_version='2024-10-21',
        azure_deployment=deployment
    )