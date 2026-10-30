import os, openai
from dotenv import load_dotenv; load_dotenv()

url, key, ver= os.environ["OPENAI_BASE_URL"].rstrip("/"), os.environ["OPENAI_API_KEY"], '2024-10-21'
print("deployments:", sorted(m.id for m in openai.AzureOpenAI(azure_endpoint=url, api_key=key, api_version=ver).models.list().data))