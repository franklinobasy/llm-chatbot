from langchain.chains import ConversationChain, ConversationalRetrievalChain, LLMChain
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ChatMessageHistory

from database.vector_store.index import initiate_index
from chatbot_v2.configs.constants import MODEL_NAME
from database.mongodb.models import PromptModel
from utilities import duration
from database.tracking.conversations import get_conversation_prompts, save_prompt

from langchain.callbacks import AsyncIteratorCallbackHandler, StdOutCallbackHandler
from langchain.callbacks.manager import AsyncCallbackManager

import asyncio

from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


@duration
def process_prompt(
    sender_id: str, conversation_id: str, prompt: str, use_history: bool = False
):
    if use_history:
        history = get_conversation_prompts(sender_id, conversation_id, k=5)
        chat_history = ChatMessageHistory()
        for qa in history:
            chat_history.add_user_message(qa[0])
            chat_history.add_ai_message(qa[1])
    else:
        chat_history = ChatMessageHistory()
        
    memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=chat_history, return_messages=True)
    
    prompt_t = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(
                "You are a nice chatbot having a conversation with a human."
            ),
            # The `variable_name` here is what must align with memory
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{question}")
        ]
    )

    llm = ChatOpenAI(model=MODEL_NAME, cache=True, temperature=0.7)

    chain = LLMChain(
        llm=llm,
        prompt=prompt_t,
        memory=memory
    )

    result = chain.invoke({"question": prompt})
    if use_history:
        
        prompt_model = PromptModel(
            question=prompt,
            answer=result['text']
        )
        save_prompt(sender_id, conversation_id, prompt_model)

    return result['text']


@duration
async def process_prompt_stream(
    sender_id: str, conversation_id: str, prompt: str, use_history: bool = False
):
    if use_history:
        history = get_conversation_prompts(sender_id, conversation_id, k=5)
        chat_history = ChatMessageHistory()
        for qa in history:
            chat_history.add_user_message(qa[0])
            chat_history.add_ai_message(qa[1])
    else:
        chat_history = ChatMessageHistory()
        
    memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=chat_history, return_messages=True)
    
    prompt_t = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(
                "You are a nice chatbot having a conversation with a human."
            ),
            # The `variable_name` here is what must align with memory
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{question}")
        ]
    )

    callback = AsyncIteratorCallbackHandler()
    llm = ChatOpenAI(model=MODEL_NAME, cache=False, temperature=1, streaming=True, callback_manager=AsyncCallbackManager([callback]))
    
    chain = LLMChain(
        llm=llm,
        prompt=prompt_t,
        memory=memory
    )
    
    task = asyncio.create_task(
        chain.ainvoke({'question': prompt})
    )

    result = ""
    try:
        async for token in callback.aiter():
            result += token
            yield token
    except Exception as e:
        pass
    finally:
        callback.done.set()

    if use_history:
        prompt_model = PromptModel(question=prompt, answer=result)
        save_prompt(sender_id, conversation_id, prompt_model)
    
    await task


@duration
async def rag_chat(
    sender_id: str, conversation_id: str, prompt: str, use_history: bool = False
):
    if use_history:
        chat_history = get_conversation_prompts(sender_id, conversation_id, k=5)
    else:
        chat_history = []
        
    callback = AsyncIteratorCallbackHandler()

    llm = ChatOpenAI(model=MODEL_NAME, cache=False, temperature=1, streaming=True, callback_manager=AsyncCallbackManager([callback]))
    index = initiate_index(id="2", store_client="chromadb", persist=True)
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=index.as_retriever(search_kwargs={"k": 4}),
    )
    
    task = asyncio.create_task(
        chain.ainvoke({'question': prompt, 'chat_history': []})
    )

    result = ""
    try:
        async for token in callback.aiter():
            result += token
            yield token
    except Exception as e:
        pass
    finally:
        callback.done.set()

    if use_history:
        prompt_model = PromptModel(question=prompt, answer=result)
        save_prompt(sender_id, conversation_id, prompt_model)
    
    await task
