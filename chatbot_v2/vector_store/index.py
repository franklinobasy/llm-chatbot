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


def load_documents(directory: str):
    ''''''
    loader = DirectoryLoader(directory)
    documents = loader.load()
    return documents


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
    persist: Annotated[bool, "Set as True or False to persist data"] = False,
    index_name: Annotated[str, "pinecone index name"] = "ccl-vectorstore",
    data_dir: Annotated[str, "Dir for dataset (documents)"] = 'data/'
) -> Union[VectorStoreIndexWrapper, Pinecone]:
    ''''''
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Path does not exist: {data_dir}")

    if not persist or index_name not in pinecone.list_indexes():
        documents = load_documents(data_dir)
        docs = split_documents(documents)

    if index_name in pinecone.list_indexes():
        if persist:
            print("Reusing index...")
            index = Pinecone.from_existing_index(
                index_name="ccl-vectorstore",
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

    return index


def get_history(sender_id: str) -> List[Tuple[str]]:
    '''
    Get sender_id chat history
    '''
    root_dir = "chat_history"
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)

    chat_file = f"{root_dir}/apichats.pkl"

    try:
        with open(chat_file, "rb") as file:
            chat_data: Dict[str, List] = pkl.load(file)
    except FileNotFoundError as e:
        with open(chat_file, "wb") as file:
            chat_data: Dict[str, List] = {}
            pkl.dump(chat_data, file)

    return [] if not chat_data.get(sender_id) else chat_data.get(sender_id)


def save_history(sender_id: str, data: List[Tuple[str]]) -> bool:
    '''
    Saves sender_id chat history
    '''
    root_dir = "chat_history"
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)

    chat_file = f"{root_dir}/apichats.pkl"
    try:
        with open(chat_file, "rb") as file:
            chat_data: dict = pkl.load(file)

        chat_data[sender_id] = data

        with open(chat_file, "wb") as file:
            pkl.dump(chat_data, file)

    except Exception as e:
        return False

    return True

