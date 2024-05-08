from langchain_openai import ChatOpenAI
from chatbot_v2.ai.tools import tools
from chatbot_v2.configs.constants import MODEL_NAME
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_functions_agent, AgentExecutor, create_react_agent

model = ChatOpenAI(
    model=MODEL_NAME,
    temperature=0.7
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a chatbot assistance for a Cyphercrescent (A software company). Your name is CCL Chatbot."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])


agent = create_openai_functions_agent(
    llm=model,
    prompt=prompt,
    tools=tools
)

agentExecutor = AgentExecutor(
    agent=agent,
    tools=tools
)

async def process_chat(agentExecutor, user_input, chat_history):
    async for event in agentExecutor.astream_events(
        {
            "input": user_input,
            "chat_history": chat_history
        },
        version="v1",
    ):
        kind = event["event"]
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                yield content
