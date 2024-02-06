# from langchain.agents import tool
# from langchain.tools.retriever import create_retriever_tool
# from langchain.memory import ConversationBufferMemory
# from langchain_openai import ChatOpenAI
# from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
# from langchain.agents import create_openai_functions_agent
# from langchain.schema import SystemMessage
# from langchain.prompts import MessagesPlaceholder

# from langchain.agents import initialize_agent, AgentExecutor

# from chatbot_v2.configs.constants import MODEL_NAME

# from database.tracking.conversations import get_conversation_prompts
# from database.vector_store.index import initiate_index

# retriever = initiate_index(id="2", store_client="chromadb", persist=True)


# @tool
# def retriever_tool(query):
#     """Searches and returns documents regarding any question"""
#     docs = retriever.similarity_search(query)
#     return docs


# @tool
# def about_cyphercrescent():
#     """Use this to tool to find out about Cyphercresect, also known as CCL"""
#     pass


# lang_retriever_tool = create_retriever_tool(
#     retriever.as_retriever(),
#     "search_documents",
#     "Searches and returns documents regarding any question",
# )

# tools = [retriever_tool]


# def call_doc_agent(
#     sender_id: str, conversation_id: str, prompt: str, use_history: bool = False
# ):
#     chat_history = get_conversation_prompts(sender_id, conversation_id)

#     memory_key = "history"
#     memory = ConversationBufferMemory(memory_key=memory_key, return_messages=True)

#     system_message = SystemMessage(
#         content=(
#             "Feel free to use any tools available to look up "
#             "relevant information, only if neccessary. If you dont have any information, dont say anything"
#         )
#     )

#     prompt_template = OpenAIFunctionsAgent.create_prompt(
#         system_message=system_message,
#         extra_prompt_messages=[MessagesPlaceholder(variable_name=memory_key)],
#     )

#     llm = ChatOpenAI(model=MODEL_NAME, cache=True, temperature=0.7)

#     # agent_executor = initialize_agent(
#     #     tools,
#     #     llm,
#     #     agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
#     #     verbose=True,
#     # )

#     agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt_template)

#     agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory)

#     result = agent_executor({"input": prompt})

#     return result["output"]
