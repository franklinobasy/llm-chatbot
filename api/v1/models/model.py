from typing import List
from pydantic import BaseModel


class Sections(BaseModel):
    '''
    Model for sections
    '''
    sections: List[str] = []


class Questions(BaseModel):
    '''
    Model for Ouestions
    '''
    section_name: str
    questions: List[str] = []


class Templates(BaseModel):
    '''
    Model for Templates
    '''
    section_name: str
    templates: List[str]


class UserInput(BaseModel):
    '''
    Model for user input
    '''
    section_id: int
    template_index: int
    answers: List[str] = []


class ProposalResult(BaseModel):
    '''
    Model for Proposal Generated
    '''
    text: str


class LetterContext(BaseModel):
    '''
    Model for letter context
    '''
    context: str


class LetterResult(BaseModel):
    '''
    Model for Letter generated
    '''
    text: str


class ChatPrompt(BaseModel):
    sender_id: str = None
    prompt: str
    use_history: bool = False