import time
from langchain.chains import ConversationalRetrievalChain, ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

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
    # index = initiate_index(id=sender_id, persist=True)
    chat_history = get_conversation_prompts(sender_id, conversation_id)
    # context = "If there isn't relevant information in the context above, use your discretion and prior knowledge to answer the user's question"

    # Initialize the LLM with the specified model name and parameters
    # Prepare memory
    memory = ConversationBufferMemory()
    for qa in chat_history:
        memory.chat_memory.add_user_message(qa[0])
        memory.chat_memory.add_ai_message(qa[1])
        
    llm = ChatOpenAI(model=MODEL_NAME, cache=True, temperature=.7)

    # Create the ConversationalRetrievalChain with the LLM and the retriever
    # chain = ConversationalRetrievalChain.from_llm(
    #     llm=llm,
    #     retriever=index.as_retriever(search_kwargs={"k": 4}),
    # )
    
    chain = ConversationChain(
        llm=llm,
        memory=memory
    )
    
    # Execute the chain to get the result
    # result = chain({"question": prompt, "chat_history": chat_history})
    result = chain.run(input=prompt)

    # chat_history.append((prompt, result['answer']))

    if use_history:
        # Save the prompt and answer to the database
        prompt_model = PromptModel(
            question=prompt,
            # answer=result["answer"]
            answer=result
        )
        save_prompt(sender_id, conversation_id, prompt_model)

    # return result['answer']
    return result

@duration
def process_prompt_2(
    sender_id: str,
    conversation_id: str,
    prompt: str,
    use_history: bool = False
):
    chat_history = get_conversation_prompts(sender_id, conversation_id, k=4)
    memory = ConversationBufferMemory()
    for qa in chat_history:
        memory.chat_memory.add_user_message(qa[0])
        memory.chat_memory.add_ai_message(qa[1])
        
    llm = ChatOpenAI(model=MODEL_NAME, cache=True, temperature=1, streaming=True)
    
    # chain = ConversationChain(
    #     llm=llm,
    #     memory=memory,
    # )
    
    result = ""
    for chunck in llm.stream(input=prompt):
        result += chunck.content
        yield chunck.content

    chat_history.append((prompt, result))
    
    if use_history:
        prompt_model = PromptModel(
            question=prompt,
            answer=result
        )
        save_prompt(sender_id, conversation_id, prompt_model)
