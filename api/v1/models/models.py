"""
API models for version 1.
"""

from typing import List, Annotated
from pydantic import BaseModel
from fastapi import File, UploadFile


class Domains(BaseModel):
    '''
    Model for Domains
    
    Attributes:
        domains (List[str]): List of domain names
    '''
    domains: List[str]
    

class Sections(BaseModel):
    """
    Model for sections.

    Attributes:
        domain_name (str): Name of the proposal domain
        sections (List[str]): List of section names.
    """
    domain_name: str
    sections: List[str] = []


class Hint(BaseModel):
    """
    Model for hint.

    Attributes:
        domain_name (str): Name of the proposal domain
        section_name (str): Name of the section.
        hint (str): hint.
    """
    domain_name: str
    section_name: str
    hint: str


class Template(BaseModel):
    """
    Model for templates.

    Attributes:
        domain_name (str): Name of proposal domain
        section_name (str): Name of the section.
        templates (List[str]): List of templates.
    """
    domain_name: str
    section_name: str
    template: str


class UserInput(BaseModel):
    """
    Model for user input.

    Attributes:
        section_id (int): ID of the section.
        template_index (int): Index of the selected template.
        answers (List[str]): List of answers to questions.
    """
    section_id: int
    template_index: int
    answers: List[str] = []


class UserInput2(BaseModel):
    """
    Model for user input.

    Attributes:
        domain_name (str): Name of proposal domin
        section_type (str): Section category
        context (str): Context for generating the section.
    """
    domain_name: str
    section_type: str
    context: str


class ProposalResult(BaseModel):
    """
    Model for generated proposals.

    Attributes:
        text (str): Generated proposal text.
    """
    text: str


class LetterContext(BaseModel):
    """
    Model for letter context.

    Attributes:
        context (str): Context for generating the letter.
    """
    context: str


class LetterResult(BaseModel):
    """
    Model for generated letters.

    Attributes:
        text (str): Generated letter text.
    """
    text: str


class ChatPrompt(BaseModel):
    """
    Model for chat prompts.

    Attributes:
        sender_id (str): Sender ID.
        conversation_id (str): Conversation ID.
        prompt (str): Prompt message.
        use_history (bool): Whether to use chat history.
    """
    sender_id: str = None
    conversation_id: str = "1"
    prompt: str
    use_history: bool = False


class UploadRequestModel(BaseModel):
    """
    Model for upload requests.

    Attributes:
        sender_id (str): Sender ID.
        files (List[UploadFile]): List of uploaded files.
    """
    sender_id: str
    files: Annotated[List[UploadFile], File(
        description="Multiple files as UploadFile")]


class BuildIndexForId(BaseModel):
    """
    Model for building index.

    Attributes:
        id (str): Identifier.
    """
    id: str


class Input(BaseModel):
    """
    Input model.

    Attributes:
        input (str): Input text.
    """
    input: str

    class Config:
        arbitrary_types_allowed = True


class Output(BaseModel):
    """
    Output model.

    Attributes:
        result (dict): Result dictionary.
    """
    result: dict


class NDAPrompt(BaseModel):
    """
    Model for NDA prompts.

    Attributes:
        answers (List): List of answers.
    """
    answers: list
