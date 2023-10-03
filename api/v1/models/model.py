from pydantic import BaseModel


class Prompt(BaseModel):
    sender_id: str = None
    prompt: str
    use_history: bool = False
