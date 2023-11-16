import dotenv
import os
import pinecone

import langchain
from langchain.cache import SQLiteCache

try:
    langchain.llm_cache = SQLiteCache(database_path=".langchain.db")
except Exception as e:
    print(e)

dotenv.load_dotenv()


pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV")
)
