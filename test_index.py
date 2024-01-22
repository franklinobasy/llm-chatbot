from chatbot_v2.configs.constants import MODEL_NAME
from chatbot_v2.vector_store.index import initiate_index
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain, ConversationalRetrievalChain
from langchain_core.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain


index = initiate_index(
    id="2",
    store_client="chromadb",
    persist=False
)

chat_history = []

llm = ChatOpenAI(model=MODEL_NAME, cache=True, temperature=.7)

chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=index.as_retriever(search_kwargs={"k": 4}),
)

while True:
    prompt = input("User 🤪: ")
    result = chain.invoke({"question": prompt, "chat_history": chat_history})
    chat_history.append((prompt, result['answer']))
    print(f"bot 🤖: {result['answer']}")
