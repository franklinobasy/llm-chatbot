# import asyncio
# from langchain.agents import tool
# from langchain.tools.retriever import create_retriever_tool
# from langchain.memory import ConversationBufferMemory, ChatMessageHistory
# from langchain_openai import ChatOpenAI
# from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
# from langchain.agents import create_openai_functions_agent
# from langchain.schema import SystemMessage
# from langchain.prompts import MessagesPlaceholder
# from langchain.callbacks import AsyncIteratorCallbackHandler
# from langchain.callbacks.manager import AsyncCallbackManager

# from langchain.agents import initialize_agent, AgentExecutor

# from chatbot_v2.configs.constants import MODEL_NAME
# from database.mongodb.models import PromptModel

# from database.tracking.conversations import get_conversation_prompts, save_prompt
# from database.vector_store.index import initiate_index


# @tool
# def retriever_tool(query):
#     """Searches and returns documents regarding any question"""
#     retriever = initiate_index(id="2", store_client="chromadb", persist=True)
#     docs = retriever.similarity_search(query)
#     return docs


# @tool
# def about_cyphercrescent():
#     """Use this to tool to find out about Cyphercresect, also known as CCL"""
#     pass


# lang_retriever_tool = create_retriever_tool(
#     initiate_index(id="1", store_client="chromadb", persist=True).as_retriever(),
#     "search_documents",
#     "Searches and returns documents regarding any question",
# )

# tools = [retriever_tool]


# class CustomAsyncIteratorCallbackHandler(AsyncIteratorCallbackHandler):
#     async def on_chat_model_start(
#         self, serialized, prompts, **kwargs
#     ) -> None:
#         # If two calls are made in a row, this resets the state
#         self.done.clear()

#     async def on_chat_model_new_token(self, token: str) -> None:
#         if token is not None and token != "":
#             self.queue.put_nowait(token)

#     async def on_chat_model_end(self, response, **kwargs) -> None:
#         self.done.set()

#     async def on_chat_model_error(self, error: BaseException, **kwargs) -> None:
#         self.done.set()


# async def call_doc_agent(
#     sender_id: str, conversation_id: str, prompt: str, use_history: bool = False
# ):
#     if use_history:
#         history = get_conversation_prompts(sender_id, conversation_id, k=5)
#         chat_history = ChatMessageHistory()
#         for qa in history:
#             chat_history.add_user_message(qa[0])
#             chat_history.add_ai_message(qa[1])
#     else:
#         chat_history = ChatMessageHistory()

#     memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=chat_history, return_messages=True)

#     system_message = SystemMessage(
#         content=(
#             "Feel free to use any tools available to look up "
#             "relevant information, only if neccessary. If you dont have any information, dont say anything"
#         )
#     )

#     prompt_template = OpenAIFunctionsAgent.create_prompt(
#         system_message=system_message,
#         extra_prompt_messages=[MessagesPlaceholder(variable_name="chat_history")],
#     )

#     callback = CustomAsyncIteratorCallbackHandler()
#     llm = ChatOpenAI(model=MODEL_NAME, cache=False, temperature=1, streaming=True, callback_manager=AsyncCallbackManager([callback]))

#     # agent_executor = initialize_agent(
#     #     tools,
#     #     llm,
#     #     agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
#     #     verbose=True,
#     # )

#     agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt_template)

#     agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory)

#     task = asyncio.create_task(
#         agent_executor.run(prompt)
#     )

#     result = ""
#     try:
#         async for token in callback.aiter():
#             result += token
#             yield token
#     except Exception as e:
#         pass
#     finally:
#         callback.done.set()

#     if use_history:
#         prompt_model = PromptModel(question=prompt, answer=result)
#         save_prompt(sender_id, conversation_id, prompt_model)

#     await task
