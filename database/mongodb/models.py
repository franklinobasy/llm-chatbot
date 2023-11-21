from datetime import datetime
from pydantic import BaseModel
from uuid import uuid4
from typing import List


class PromptModel(BaseModel):
    question: str
    answer: str
    

class ConversationModel(BaseModel):
    date_created: datetime = datetime.utcnow()
    date_modified: datetime = datetime.utcnow()
    conversation_id: str = uuid4().hex
    prompts: List[PromptModel] = []


class UserModel(BaseModel):
    user_id: str = str(uuid4().hex)
    conversations: List[ConversationModel] = []

