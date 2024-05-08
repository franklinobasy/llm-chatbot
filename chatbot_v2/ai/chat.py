"""
Module: chat.py

This module contains functions for processing prompts and conducting chats using various methods such as retrieval-aided generation (RAG) and Guardrail mechanism.

Functions:
    - process_prompt: Process a single prompt in a synchronous manner.
    - process_prompt_stream: Process a single prompt in an asynchronous manner with streaming.
    - rag_chat: Conduct a chat using Retrieval-Aided Generation (RAG) method.
    - guardrail_chat: Conduct a chat using Guardrail mechanism.
"""

from langchain.chains import ConversationalRetrievalChain, LLMChain, RetrievalQA
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ChatMessageHistory

from database.vector_store.index import initiate_index
from chatbot_v2.configs.constants import MODEL_NAME
from utilities import duration

from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.callbacks.manager import AsyncCallbackManager

import asyncio

from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from guardrails.configs.config import guardrail_app

from chatbot_v2.ai.chat_agent import agentExecutor, agent


@duration
def process_prompt(
    sender_id: str, conversation_id: str, prompt: str
):
    """
    Process a single prompt in a synchronous manner.

    Parameters:
        sender_id (str): ID of the sender.
        conversation_id (str): ID of the conversation.
        prompt (str): The prompt to process.

    Returns:
        str: The response generated for the prompt.
    """
    # Initialize chat history memory
    chat_history = ChatMessageHistory()
    memory = ConversationBufferMemory(
        memory_key="chat_history", chat_memory=chat_history, return_messages=True)

    # Define chat prompt template
    prompt_t = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(
                "You are a nice chatbot having a conversation with a human."
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{question}")
        ]
    )

    # Initialize ChatOpenAI model
    llm = ChatOpenAI(model=MODEL_NAME, cache=True, temperature=0.7)

    # Initialize LLMChain with ChatOpenAI model and memory
    chain = LLMChain(
        llm=llm,
        prompt=prompt_t,
        memory=memory
    )

    # Invoke the chain with the prompt
    result = chain.invoke({"question": prompt})

    return result['text']


@duration
async def process_prompt_stream(
    sender_id: str, conversation_id: str, prompt: str
):
    """
    Process a single prompt in an asynchronous manner with streaming.

    Parameters:
        sender_id (str): ID of the sender.
        conversation_id (str): ID of the conversation.
        prompt (str): The prompt to process.

    Yields:
        str: A chunk of the response generated for the prompt.
    """
    # Initialize chat history memory
    chat_history = ChatMessageHistory()
    memory = ConversationBufferMemory(
        memory_key="chat_history", chat_memory=chat_history, return_messages=True)

    # Define chat prompt template
    prompt_t = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(
                "You are a nice chatbot having a conversation with a human."
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{question}")
        ]
    )

    # Initialize ChatOpenAI model with asynchronous streaming
    callback = AsyncIteratorCallbackHandler()
    llm = ChatOpenAI(model=MODEL_NAME, cache=False, temperature=1,
                     streaming=True, callback_manager=AsyncCallbackManager([callback]))

    # Initialize LLMChain with ChatOpenAI model, prompt template, and memory
    chain = LLMChain(
        llm=llm,
        prompt=prompt_t,
        memory=memory
    )

    # Invoke the chain asynchronously with the prompt
    task = asyncio.create_task(
        chain.ainvoke({'question': prompt})
    )

    # Stream the response asynchronously
    try:
        async for token in callback.aiter():
            yield token
    finally:
        callback.done.set()

    await task


@duration
async def rag_chat(
    sender_id: str, conversation_id: str, prompt: str
):
    """
    Conduct a chat using Retrieval-Aided Generation (RAG) method.

    Parameters:
        sender_id (str): ID of the sender.
        conversation_id (str): ID of the conversation.
        prompt (str): The prompt to process.

    Yields:
        str: A chunk of the response generated for the prompt.
    """
    # Initialize callback handler for asynchronous streaming
    callback = AsyncIteratorCallbackHandler()

    # Initialize ChatOpenAI model with asynchronous streaming
    llm = ChatOpenAI(model=MODEL_NAME, cache=False, temperature=1,
                     streaming=True, callback_manager=AsyncCallbackManager([callback]))

    # Initialize conversation index for retrieval
    index = initiate_index(id=sender_id, store_client="chromadb", persist=True)

    # Initialize ConversationalRetrievalChain with ChatOpenAI model and conversation retriever
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=index.as_retriever(search_kwargs={"k": 4}),
    )

    # Invoke the chain asynchronously with the prompt
    task = asyncio.create_task(
        chain.ainvoke({'question': prompt, 'chat_history': []})
    )

    # Stream the response asynchronously
    try:
        async for token in callback.aiter():
            yield token
    finally:
        callback.done.set()

    await task


@duration
async def guardrail_chat(
    sender_id: str, conversation_id: str, prompt: str, use_history: bool = False
):
    """
    Conduct a chat using Guardrail mechanism.

    Parameters:
        sender_id (str): ID of the sender.
        conversation_id (str): ID of the conversation.
        prompt (str): The prompt to process.
        use_history (bool): Whether to use chat history in the conversation.

    Yields:
        str: A chunk of the response generated for the prompt.
    """
    # Initialize conversation index for retrieval
    # index = initiate_index(id=sender_id, store_client="chromadb", persist=True)

    # Initialize RetrievalQA chain with Guardrail application settings
    # qa_ccl_chain = RetrievalQA.from_chain_type(
    #     llm=guardrail_app.llm,
    #     chain_type="stuff",
    #     retriever=index.as_retriever(search_kwargs={"k": 4}),
    # )
    # guardrail_app.register_action(qa_ccl_chain, name="qa_ccl_chain")
    guardrail_app.register_action(agent, name="qa_ccl_chain")

    # Initialize chat history
    history = [{"role": "user", "content": f"{prompt}"}]

    # Stream the response asynchronously
    async for chunk in guardrail_app.stream_async(messages=history):
        yield chunk
