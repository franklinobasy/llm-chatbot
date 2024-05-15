"""
Module for managing document indexing and storage.

This module provides functions for loading, splitting, and indexing documents using different vector storage services like Pinecone and Chroma.

Attributes:
    - chat_history_root_dir (str): The root directory for storing chat history documents.
    - bucket_util: An instance of the BucketUtil class for managing files in an S3 bucket.

Functions:
    - load_documents(directory: str) -> List[str]: Load documents from the specified directory.
    - split_documents(documents, chunk_size: int = 2000) -> List[str]: Split documents into chunks for efficient indexing.
    - initiate_index(id: str = None, persist: bool = False, store_client: str = "pinecone"): Initialize an index for document storage.
    - pinecone_store(id, index_name: str = None, persist: bool = None, data_dir: str = None): Store documents using the Pinecone vector store.
    - chromadb_store(id, collection_name, persist, data_dir, db_directory="chroma_persist_directory"): Store documents using the Chroma vector store.
"""


from typing import Annotated, Any, List, Union
import time
import logging
import os
import chromadb

from langchain_community.document_loaders.directory import DirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.pinecone import Pinecone
from langchain_community.vectorstores.chroma import Chroma

from database.vector_store import pinecone
from utilities import duration
from utilities.aws_tools import BucketUtil

# Set up the root directory for chat history storage
chat_history_root_dir = "../chat_history"

# Initialize BucketUtil for managing files in the S3 bucket
bucket_util = BucketUtil(bucket_name="ccl-chatbot-document-store")


def load_documents(directory: str) -> List[str]:
    """
    Load documents from the specified directory.

    Parameters:
        directory (str): The directory path from which to load documents.

    Returns:
        List[str]: A list of strings representing the loaded documents.
    """
    loader = DirectoryLoader(directory)
    documents = loader.load()
    return documents


def split_documents(documents, chunk_size: int = 2000) -> List[str]:
    """
    Split documents into chunks for efficient indexing.

    Parameters:
        documents: The documents to split.
        chunk_size (int, optional): The size of each chunk (default is 2000).

    Returns:
        List[str]: A list of strings representing the split document chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size)
    docs = text_splitter.split_documents(documents)
    return docs


def initiate_index(id: str = None, persist: bool = False, store_client: str = "pinecone"):
    """
    Initialize an index for document storage.

    Parameters:
        id (str, optional): The ID for the index (default is None).
        persist (bool, optional): Set to True to persist data (default is False).
        store_client (str, optional): The client for storing documents (default is "pinecone").

    Returns:
        Any: The initialized index for document storage.
    """
    data_dir = os.path.join(os.getcwd(), "bin", id)
    store_name = f"tempuser-{id}"

    if store_client == "pinecone":
        return pinecone_store(
            id,
            persist,
            data_dir,
            index_name="ccl-vectorstore",
        )
    elif store_client == "chromadb":
        return chromadb_store(
            id,
            collection_name=store_name,
            persist=persist,
            data_dir=data_dir,
        )


def pinecone_store(
    id,
    index_name: str = None,
    persist: bool = None,
    data_dir: str = None
) -> Any:
    """
    Initialize or reuse a Pinecone index for document storage.

    Parameters:
        id: The ID for the index.
        index_name (str, optional): The name of the index (default is None).
        persist (bool, optional): Set to True to persist data (default is None).
        data_dir (str, optional): The directory path containing documents (default is None).

    Returns:
        Any: The initialized or reused Pinecone index.
    """
    if not persist or index_name not in pinecone.list_indexes():
        bucket_util.download_files(id)
        documents = load_documents(data_dir)
        docs = split_documents(documents)

    if index_name in pinecone.list_indexes():
        if persist:
            print("Reusing index...")
            index = Pinecone.from_existing_index(
                index_name=index_name, embedding=OpenAIEmbeddings()
            )
            return index
        else:
            logging.warning(
                """
                Index exist but has not been persisted.
                Deleting previous index and create a new one
                """
            )

            logging.info(f"Deleting index with name: {index_name}")
            pinecone.delete_index(index_name)
            logging.info(f"Successfully deleted index with name: {index_name}")

            logging.info(f"Creating new index with name: {index_name}")
            pinecone.create_index(name=index_name, dimension=1536)

            # Wait for index to be created
            while not pinecone.describe_index(index_name).status["ready"]:
                time.sleep(1)

            logging.info(f"Successfully created new index with name: {index_name}")

            index = Pinecone.from_documents(
                docs, embedding=OpenAIEmbeddings(), index_name=index_name
            )
    else:
        logging.info(f"Creating new index with name: {index_name}")
        pinecone.create_index(name=index_name, dimension=1536)

        # Wait for index to be created
        while not pinecone.describe_index(index_name).status["ready"]:
            time.sleep(1)

        logging.info(f"Successfully created new index with name: {index_name}")

        index = Pinecone.from_documents(
            docs, embedding=OpenAIEmbeddings(), index_name=index_name
        )

    if not persist:
        # clear bin
        bucket_util.delete_from_bin(id)

    return index


def chromadb_store(
    id,
    collection_name: str,
    persist: bool,
    data_dir: str,
    db_directory: str = "chroma_persist_directory"
) -> Union[Chroma, None]:
    """
    Initialize or reuse a ChromaDB collection for document storage.

    Parameters:
        id: The ID for the collection.
        collection_name (str): The name of the collection.
        persist (bool): Set to True to persist data.
        data_dir (str): The directory path containing documents.
        db_directory (str, optional): The directory path for persisting data (default is "chroma_persist_directory").

    Returns:
        Union[Chroma, None]: The initialized or reused ChromaDB collection, or None if persist is True.
    """
    if not persist:
        bucket_util.download_files(id)
        print(" index...")
        documents = load_documents(data_dir)
        docs = split_documents(documents)

        db = Chroma.from_documents(
            docs,
            embedding=OpenAIEmbeddings(),
            collection_name=collection_name,
            persist_directory=db_directory,
        )

        # clear bin
        bucket_util.delete_from_bin(id)

        return db

    client = chromadb.PersistentClient(path=db_directory)

    db = Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=OpenAIEmbeddings(),
    )

    return db
