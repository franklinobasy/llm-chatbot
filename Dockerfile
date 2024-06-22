FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV OPENAI_API_KEY ""
ENV PINECONE_API_KEY ""
ENV PINECONE_ENV ""
ENV AWS_ACCESS_KEY ""
ENV AWS_SECRET_ACCESS_KEY ""
ENV MONGO_DB_USERNAME ""
ENV MONGO_DB_PASSWORD ""
ENV ENV ""
ENV LANGCHAIN_TRACING_V2 ""
ENV LANGCHAIN_API_KEY ""

WORKDIR /llm-chatbot

RUN apt-get update && \
    apt-get install -y git python3-dev gcc g++ && \
    rm -rf /var/lib/apt/lists/* && \
    git clone -b version-2c https://github.com/franklinobasy/llm-chatbot.git .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
