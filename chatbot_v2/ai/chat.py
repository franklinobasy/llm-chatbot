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
    chat_history = get_conversation_prompts(sender_id, conversation_id)
    context = "If there isn't relevant information in the context above, use your discretion and prior knowledge to answer the user's question"

    # Initialize the LLM with the specified model name and parameters
    llm = ChatOpenAI(model=MODEL_NAME, cache=True, temperature=1)

    # Create the ConversationalRetrievalChain with the LLM and the retriever
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=index.as_retriever(search_kwargs={"k": 4}),
    )

    # Execute the chain to get the result
    result = chain({"context": context, "question": prompt, "chat_history": chat_history})

    chat_history.append((prompt, result['answer']))

    if use_history:
        # Save the prompt and answer to the database
        prompt_model = PromptModel(
            question=prompt,
            answer=result["answer"]
        )
        save_prompt(sender_id, conversation_id, prompt_model)

    return result['answer']
