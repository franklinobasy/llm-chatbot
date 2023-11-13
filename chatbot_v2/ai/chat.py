from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

from chatbot_v2.vector_store.index import get_history, initiate_index, save_history
from chatbot_v2.configs.constants import MODEL_NAME


def process_prompt(sender_id: str, prompt: str, use_history: bool = False):
    index = initiate_index(persist=True)
    model = MODEL_NAME
    chat_history = get_history(sender_id) if use_history else []

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model=model, cache=True),
        retriever=index.as_retriever(search_kwargs={"k": 1}),
    )

    result = chain({"question": prompt, "chat_history": chat_history})
    chat_history.append((prompt, result['answer']))

    if use_history:
        save_history(sender_id, chat_history)

    return result['answer']
