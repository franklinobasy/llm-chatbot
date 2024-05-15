from langchain.agents import tool
from langchain.tools.retriever import create_retriever_tool
from chatbot_v2.configs.constants import MODEL_NAME
from database.vector_store.index import initiate_index


# @tool
# def retriever_tool(query):
#     """Searches and returns documents regarding any question"""
#     retriever = initiate_index(id="2", store_client="chromadb", persist=True)
#     docs = retriever.similarity_search(query)
#     return docs


@tool
def about_cyphercrescent(query):
    """Use this to tool to answer any question that relates Cyphercresect, also known as CCL"""
    retriever = initiate_index(id="1", store_client="chromadb", persist=True)
    docs = retriever.similarity_search(query)
    return docs


# lang_retriever_tool = create_retriever_tool(
#     initiate_index(id="1", store_client="chromadb", persist=True).as_retriever(),
#     "search_documents",
#     "Searches and returns documents regarding any question",
# )

tools = [about_cyphercrescent]
