from fastapi import File, UploadFile

from typing import Annotated, List, Optional
from pydantic import BaseModel


class Sections(BaseModel):
    """
    Model for sections
    """

    sections: List[str] = []


class Questions(BaseModel):
    """
    Model for Ouestions
    """

    section_name: str
    questions: List[str] = []


class Templates(BaseModel):
    """
    Model for Templates
    """

    section_name: str
    templates: List[str]


class UserInput(BaseModel):
    """
    Model for user input
    """

    section_id: int
    template_index: int
    answers: List[str] = []
    

class UserInput2(BaseModel):
    """
    Model for user input
    """

    section_id: int
    template_index: int = -1
    context: str


class ProposalResult(BaseModel):
    """
    Model for Proposal Generated
    """

    text: str


class LetterContext(BaseModel):
    """
    Model for letter context
    """

    context: str


class LetterResult(BaseModel):
    """
    Model for Letter generated
    """

    text: str


class ChatPrompt(BaseModel):
    sender_id: str = None
    conversation_id: str = "1"
    prompt: str
    use_history: bool = False


class UploadRequestModel(BaseModel):
    sender_id: str
    files: Annotated[list[UploadFile], File(description="Multiple files as UploadFile")]


class BuildIndexForId(BaseModel):
    id: str


class Input(BaseModel):
    input: str

    class Config:
        arbitrary_types_allowed = True


class Output(BaseModel):
    # Define your output fields here
    result: dict


class NDAPrompt(BaseModel):
    answers: list
