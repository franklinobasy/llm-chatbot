"""
Module for initializing the vector store.

This module initializes the vector store for storing and querying language models.

Attributes:
    - pinecone: A Pinecone object for interacting with the Pinecone vector store service.

"""

import dotenv
import os
from pinecone import Pinecone

import langchain
from langchain.cache import SQLiteCache

# Set up language model caching
langchain.llm_cache = SQLiteCache(database_path=".langchain.db")

dotenv.load_dotenv()

# Initialize Pinecone vector store
pinecone = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENV")
)
