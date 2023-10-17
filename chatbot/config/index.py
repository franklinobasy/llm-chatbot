import dotenv
import logging
import os
import pickle as pkl
from typing import Annotated, Optional, Dict, List, Tuple, Union


from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone

import pinecone

dotenv.load_dotenv()

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV")
)


def load_documents(directory: str):
    loader = DirectoryLoader(directory)
    documents = loader.load()
    return documents


def split_documents(
    documents,
    chunk_size=2000,
):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
    )
    docs = text_splitter.split_documents(documents)
    return docs


def initiate_index(
    persist: Annotated[bool, "Set as True or False to persist data"] = False,
    index_name: Annotated[str, "pinecone index name"] = "ccl-vectorstore",
    data_dir: Annotated[str, "Dir for dataset (documents)"] = 'data/'
) -> Pinecone:
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Path does not exist: {data_dir}")

    documents = load_documents(data_dir)
    docs = split_documents(documents)

    if index_name in pinecone.list_indexes():
        if persist:
            logging.info("Reusing index...")
            index = Pinecone.from_existing_index(
                index_name="ccl-vectorstore",
                embedding=OpenAIEmbeddings()
            )
            return index
        else:
            logging.info(f'Deleting index with name: {index_name}')
            pinecone.delete_index(index_name)
            logging.info(f'Successfully deleted index with name: {index_name}')

            logging.info(f"Creating new index with name: {index_name}")
            pinecone.create_index(
                name=index_name,
                dimension=1536
            )
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