from typing import Annotated, Dict, List, Tuple, Union
import time
import logging
import os
import pickle as pkl


from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone

from chatbot_v2.vector_store import pinecone
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
) -> Union[VectorStoreIndexWrapper, Pinecone]:
    ''''''
    data_dir = os.path.join(os.getcwd(), "bin", id)
    # index_name = f"tempuser-{id}"
    index_name = "ccl-vectorstore"

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
