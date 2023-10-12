import langchain

from chatbot.config.index import initiate_index, get_history, save_history
from langchain.cache import SQLiteCache
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from chatbot.auto_response.prompts import PROMPT


langchain.llm_cache = SQLiteCache(database_path=".langchain.db")


def process_prompt(sender_id: str, prompt: str, use_history: bool = False):
    index = initiate_index(persist=True)
    model = "gpt-3.5-turbo-0301"
    chat_history = get_history(sender_id) if use_history else []

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model=model, cache=True),
        retriever=index.as_retriever(search_kwargs={"k": 1}),
        combine_docs_chain_kwargs={
                "prompt": PROMPT
            }
    )

    result = chain({"question": prompt, "chat_history": chat_history})
    chat_history.append((prompt, result['answer']))

    if use_history:
        save_history(sender_id, chat_history)

    return result['answer']
