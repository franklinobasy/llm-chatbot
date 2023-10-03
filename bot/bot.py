#!/bin/python3

'''
Conversational chat bot that leverages on OpenAi GPT-X model
'''

import dotenv
import os
import pickle as pkl
import sys
from typing import Annotated, Optional, Dict, List, Tuple

from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma


dotenv.load_dotenv()


def initiate_index(
    persist: Annotated[bool, "Set as True or False to persist data"] = False,
    persist_dir: Annotated[str, "Dir to store persisted data"] = "persist",
    data_dir: Annotated[str, "Dir for dataset (documents)"] = 'data/'
) -> VectorStoreIndexWrapper:
    if persist and os.path.exists(persist_dir):
        print("Reusing index...\n")
        vectorstore = Chroma(
            persist_directory=persist_dir,
            embedding_function=OpenAIEmbeddings()
        )
        index = VectorStoreIndexWrapper(vectorstore=vectorstore)
    else:
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        loader = DirectoryLoader(data_dir)

        if persist:
            if not os.path.exists(persist_dir):
                os.makedirs(persist_dir)

            index = VectorstoreIndexCreator(
                vectorstore_kwargs={
                    "persist_directory": persist_dir
                },
                embedding=OpenAIEmbeddings(),
            ).from_loaders([loader])
        else:
            index = VectorstoreIndexCreator(
                embedding=OpenAIEmbeddings()
            ).from_loaders([loader])
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


def get_prompt(sender_id: str, prompt: str, use_history: bool = False):
    index = initiate_index()
    model = "gpt-3.5-turbo-0301"
    chat_history = get_history(sender_id) if use_history else []

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model=model),
        retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
    )

    result = chain({"question": prompt, "chat_history": chat_history})
    chat_history.append((prompt, result['answer']))
    save_history(sender_id, chat_history)

    return result['answer']


def main(
    model: Annotated[Optional[str], "Choose the model"] = "gpt-3.5-turbo",
    load_history: Annotated[Optional[bool], "Load chat history"] = False,
) -> None:

    # Create index from vector store
    index = initiate_index(
        persist=False
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model=model),
        retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
    )
    if not load_history:
        chat_history = []
    else:
        try:
            with open("./chat_history/chats.pkl", "rb") as file_object:
                chat_history = pkl.load(file_object)
        except FileNotFoundError as e:
            print("No chat history found. Starting a new chat...")
            chat_history = []

    query: str = None
    if len(sys.argv) > 1:
        query = sys.argv[1]

    # Chat runs as loop to keep the terminal active
    while True:
        if not query:
            query = input("Prompt: ")
        if query in ['quit', 'q', 'exit']:
            # save chat history
            if load_history:
                try:
                    with open("./chat_history/chats.pkl", "wb") as file_object:
                        pkl.dump(chat_history, file_object)
                except Exception as e:
                    print(e)
                finally:
                    sys.exit()
            else:
                sys.exit()
        result = chain({"question": query, "chat_history": chat_history})
        print(result['answer'])

        chat_history.append((query, result['answer']))
        query = None
