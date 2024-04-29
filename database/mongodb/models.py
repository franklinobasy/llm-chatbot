"""
Module: database.mongodb.models

The `models.py` module defines Pydantic models for representing data structures used in MongoDB collections.

Classes:
    - PromptModel: Pydantic model for representing a prompt with a question and its corresponding answer.
    - ConversationModel: Pydantic model for representing a conversation with its metadata and prompts.
    - UserModel: Pydantic model for representing a user with their ID and associated conversations.

Usage:
    from database.mongodb.models import PromptModel, ConversationModel, UserModel

    # Example usage of models
    prompt = PromptModel(question="What is your name?", answer="My name is John.")
    conversation = ConversationModel(conversation_name="Greetings", prompts=[prompt])
    user = UserModel(user_id="123", conversations=[conversation])
"""
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import uuid4
from typing import List

class PromptModel(BaseModel):
    """
    Pydantic model for representing a prompt with a question and its corresponding answer.

    Attributes:
        - question (str): The question prompt.
        - answer (str): The answer corresponding to the question.
    """

    question: str
    answer: str


class ConversationModel(BaseModel):
    """
    Pydantic model for representing a conversation with its metadata and prompts.

    Attributes:
        - date_created (datetime): The date and time when the conversation was created.
        - date_modified (datetime): The date and time when the conversation was last modified.
        - conversation_name (str): The name of the conversation.
        - conversation_id (str): The unique ID of the conversation.
        - prompts (List[PromptModel]): List of prompt models associated with the conversation.
    """

    date_created: datetime = Field(default_factory=datetime.utcnow)
    date_modified: datetime = Field(default_factory=datetime.utcnow)
    conversation_name: str = "New conversation"
    conversation_id: str = Field(default_factory=lambda: uuid4().hex)
    prompts: List[PromptModel] = []


class UserModel(BaseModel):
    """
    Pydantic model for representing a user with their ID and associated conversations.

    Attributes:
        - user_id (str): The unique ID of the user.
        - conversations (List[ConversationModel]): List of conversation models associated with the user.
    """

    user_id: str = Field(default_factory=lambda: uuid4().hex)
    conversations: List[ConversationModel] = []
