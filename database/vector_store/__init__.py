import dotenv
import os
from pinecone import Pinecone

import langchain
from langchain.cache import SQLiteCache

langchain.llm_cache = SQLiteCache(database_path=".langchain.db")

dotenv.load_dotenv()


pinecone = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENV")
)
