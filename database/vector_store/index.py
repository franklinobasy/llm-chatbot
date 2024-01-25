from typing import Annotated, Dict, List, Tuple, Union
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


chat_history_root_dir = "../chat_history"
bucket_util = BucketUtil(bucket_name="ccl-chatbot-document-store")


@duration
def load_documents(directory: str):
    ''''''
    loader = DirectoryLoader(directory)
    documents = loader.load()
    return documents


@duration
def split_documents(
    documents,
    chunk_size=2000,
):
    ''''''
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
    )
    docs = text_splitter.split_documents(documents)
    return docs


@duration
def initiate_index(
    id: str = None,
    persist: Annotated[bool, "Set as True or False to persist data"] = False,
    store_client = "pinecone",
):
    ''''''
    data_dir = os.path.join(os.getcwd(), "bin", id)
    store_name = f"tempuser-{id}"
    
    if store_client == "pinecone":
        return pinecone_store(
            id,
            persist,
            data_dir,
            index_name = "ccl-vectorstore",
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
    index_name: str  = None,
    persist: bool = None,
    data_dir: str = None
):
    if not persist or index_name not in pinecone.list_indexes():
        bucket_util.download_files(id)
        documents = load_documents(data_dir)
        docs = split_documents(documents)

    if index_name in pinecone.list_indexes():
        if persist:
            print("Reusing index...")
            index = Pinecone.from_existing_index(
                index_name=index_name,
                embedding=OpenAIEmbeddings()
            )
            return index
        else:
            logging.warning(
                '''
                Index exist but has not been persisted.
                Deleting previous index and create a new one
                '''
            )

            logging.info(f'Deleting index with name: {index_name}')
            pinecone.delete_index(index_name)
            logging.info(f'Successfully deleted index with name: {index_name}')

            logging.info(f"Creating new index with name: {index_name}")
            pinecone.create_index(
                name=index_name,
                dimension=1536
            )

            # Wait for index to be created
            while not pinecone.describe_index(index_name).status['ready']:
                time.sleep(1)
            
            logging.info(
                f"Successfully created new index with name: {index_name}"
            )

            index = Pinecone.from_documents(
                docs,
                embedding=OpenAIEmbeddings(),
                index_name=index_name
            )
    else:
        logging.info(f"Creating new index with name: {index_name}")
        pinecone.create_index(
            name=index_name,
            dimension=1536
        )

        # Wait for index to be created
        while not pinecone.describe_index(index_name).status['ready']:
            time.sleep(1)

        logging.info(f"Successfully created new index with name: {index_name}")

        index = Pinecone.from_documents(
            docs,
            embedding=OpenAIEmbeddings(),
            index_name=index_name
        )
    
    if not persist:
        # clear bin
        bucket_util.delete_from_bin(id)

    return index


def chromadb_store(
    id,
    collection_name,
    persist,
    data_dir,
    db_directory = "chroma_persist_directory",
):
    if not persist:
        bucket_util.download_files(id)
        documents = load_documents(data_dir)
        docs = split_documents(documents)
        
        db = Chroma.from_documents(
            docs,
            embedding=OpenAIEmbeddings(),
            collection_name=collection_name,
            persist_directory=db_directory
        )
        
        # clear bin
        bucket_util.delete_from_bin(id)
        
        return db
    
    client = chromadb.PersistentClient(path=db_directory)
    
    db = Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=OpenAIEmbeddings()
    )
    
    return db
