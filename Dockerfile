FROM python:3.10-slim AS build

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y git
RUN git clone -b dev https://github.com/franklinobasy/llm-chatbot.git /llm-chatbot
RUN pip install --no-cache-dir -r /llm-chatbot/requirements.txt

WORKDIR /llm-chatbot

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
