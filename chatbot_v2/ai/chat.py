from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

from chatbot_v2.vector_store.index import initiate_index
from chatbot_v2.configs.constants import MODEL_NAME
from database.mongodb.models import PromptModel
from utilities import duration
from database.tracking.conversations import (
    get_conversation_prompts,
    save_prompt
)


@duration
def process_prompt(
    sender_id: str,
    conversation_id: str,
    prompt: str,
    use_history: bool = False
):
    index = initiate_index(id=sender_id, persist=True)
    model = MODEL_NAME
    chat_history = get_conversation_prompts(sender_id, conversation_id)

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model=model, cache=True),
        retriever=index.as_retriever(search_kwargs={"k": 1}),
    )

    result = chain({"question": prompt, "chat_history": chat_history})
    chat_history.append((prompt, result['answer']))

    if use_history:
        prompt = PromptModel(
            question=prompt,
            answer=result["answer"]
        )
        save_prompt(sender_id, conversation_id, prompt)

    return result['answer']
