#!/bin/python3
import os
from typing import Annotated, Dict
from fastapi import (
    Body,
    File,
    Query,
    UploadFile,
    APIRouter,
    HTTPException,
)
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

from api.v1.models.models import (
    BuildIndexForId,
    ChatPrompt,
    Domains,
    Input,
    LetterContext,
    LetterResult,
    NDAPrompt,
    ProposalResult,
    Hint,
    Sections,
    Template,
    UserInput,
    UploadRequestModel,
    UserInput2,
)
from api.v1.routes.error_handler import (
    AnswersMisMatchQuestion,
    PathTypeMisMatch,
    UnknownSection,
    UnknownSectionName,
    UnknownTemplateID,
    VectorIndexError,
)
from chatbot_v2.ai.chat import (
    guardrail_chat,
    process_prompt,
    process_prompt_stream,
    rag_chat
)
# from chatbot_v2.ai.chat_agent import call_doc_agent
from chatbot_v2.ai.chat_agent import (
    agentExecutor,
    process_chat as agent_chat,
)
from chatbot_v2.ai.generate_proposal import AutoFillTemplate
from chatbot_v2.ai.generate_letter import AutoWriteLetter
from chatbot_v2.ai.generate_nda import GenerateNDA, templates
from chatbot_v2.ai.generate_proposal_2 import AutoGenerateSection
from chatbot_v2.ai.style_engine import StyleGuide
from chatbot_v2.configs.constants import MODEL_NAME
from chatbot_v2.handlers.field_handler import FieldHandler
from chatbot_v2.handlers.template_handler import TemplateHandler
from chatbot_v2.templates.domains import DOMAINS
from database.vector_store.index import initiate_index
from chatbot_v2.templates.context_config import (
    CHAT_SYSTEM_PROMPT,
)
from utilities.aws_tools import BucketUtil
from uuid import uuid4

router = APIRouter()
bucket_util = BucketUtil(bucket_name="ccl-chatbot-document-store")


@router.get('/proposal_domains', response_model=Domains)
async def get_all_proposal_domains():
    """Get all available proposal domain names
    
    Returns:
        Domains: A response containing a list of available proposal domains
    """
    domains = DOMAINS.keys()
    return Domains(domains=list(domains))


class SectionsRequest(BaseModel):
    domain_name: str

@router.post("/sections", response_model=Sections)
async def get_all_sections(request: SectionsRequest = Body(...)):
    """Get all available sections in a proposal domain.

    Returns:
        SectionsResponse: A response containing a list of available sections.
    """
    domain_name = request.domain_name
    if domain_name not in DOMAINS:
        raise HTTPException(status_code=400, detail=f'{domain_name} is not supported.')
    
    sections = DOMAINS[domain_name].keys()
    return Sections(domain_name=domain_name, sections=list(sections))


class HintRequest(BaseModel):
    domain_name: str

@router.post("/hint/{section_type}", response_model=Hint)
async def get_section_hint(section_type: str, request: HintRequest = Body(...)):
    """Get questions for a specific section."""
    domain_name = request.domain_name
    th = TemplateHandler(domain_name, section_type)
    hint = th.get_hint()
    return Hint(
        domain_name=domain_name,
        section_name=section_type,
        hint=hint
    )


class TemplateRequest(BaseModel):
    domain_name: str
    section_type: str


@router.post("/templates", response_model=Template)
async def get_section_templates(request: TemplateRequest = Body(...)):
    """Get templates for a specific section.

    Args:
        request (TemplateRequest): A request containing the domain name and section type.

    Returns:
        TemplateResponse: A response containing the domain name, section name, and the template.
    """
    domain_name = request.domain_name
    section_type = request.section_type

    
    th = TemplateHandler(domain_name, section_type)
    template = th.get_template()
    
    return Template(
        domain_name=domain_name,
        section_name=section_type,
        template=template
    )


@router.post("/generate")
async def generate_proposal(user_input: UserInput):
    """Generate a proposal based on user input.

    Args:
        user_input (UserInput): User input data including
        section ID, template index, and answers.

    Returns:
        ProposalResult: A response containing the generated proposal text.

    Raises:
        UnknownSectionID: If the section ID is out of range.
        UnknownTemplateID: If the template index is out of range.
        AnswersMisMatchQuestion: If the number of answers does not
        match the number of questions.
    """
    section_id = user_input.section_id
    template_index = user_input.template_index
    answers = user_input.answers

    try:
        section_name = list(section_templates.keys())[section_id]
    except IndexError as _:
        raise UnknownSectionID(section_id)

    template_store = TemplateHandler(section_name)

    try:
        template = template_store.get_templates()[template_index]
    except IndexError:
        raise UnknownTemplateID(template_index)

    try:
        question_handler = QuestionHandler(section_name)
        questions_answers = question_handler.set_answers(answers)
    except ValueError as _:
        raise AnswersMisMatchQuestion(
            n_questions=len(
                question_handler.get_questions()
            ), n_answers=len(answers)
        )

    # Field selection section
    fh = FieldHandler(template)

    # # Get all the fields in the selected template
    fields = fh.get_fields_from_template()

    # LLM section
    bot = AutoFillTemplate(MODEL_NAME)

    # using the questions, answers and the field, the bot
    # is used to fill the fields with the appropriate answers
    # and stores the result in a dictionary
    filled_fields = bot.fill_fields(fields, questions_answers)

    # the filled fields are inserted into the template
    filled_templates = fh.fill_template(filled_fields)

    return ProposalResult(text=filled_templates)


@router.post("/generate/proposal")
async def generate_proposal(user_input: UserInput2):
    """Version 2: Generate a proposal section"""
    domain_name = user_input.domain_name
    section_type = user_input.section_type
    context = user_input.context

    generator = AutoGenerateSection(MODEL_NAME, domain_name, section_type)

    # prepare template
    generator.set_template()

    result = generator.generate_section(context)
    return result


@router.post("/generate/proposal/stream")
async def generate_proposal_2(user_input: UserInput2):
    """Version 2: [Stream] Generate a proposal section"""
    domain_name = user_input.domain_name
    section_type = user_input.section_type
    context = user_input.context

    generator = AutoGenerateSection(MODEL_NAME, domain_name, section_type)

    generator.set_template()

    return StreamingResponse(
        generator.generate_controller(context), media_type="text/event-stream"
    )


@router.post("/letter")
def write_letter(letter_context: LetterContext):
    """Write a letter based on the provided context.

    Args:
        letter_context (LetterContext): Context data for generating the letter.

    Returns:
        LetterResult: A response containing the generated letter text.
    """
    context = letter_context.context
    llm = AutoWriteLetter(MODEL_NAME)
    generated_letter = llm.generate(context)
    return LetterResult(text=generated_letter)


@router.post("/letter/stream")
def write_letter_2(letter_context: LetterContext):
    """Version 2: [Stream] Write a letter based on the provided context.

    Args:
        letter_context (LetterContext): Context data for generating the letter.

    Returns:
        LetterResult: A response containing the generated letter text.
    """
    context = letter_context.context
    llm = AutoWriteLetter(MODEL_NAME)
    return StreamingResponse(
        llm.generate_2(context),
        media_type="text/event-stream"
    )


@router.post("/chat")
async def chat(request: ChatPrompt):
    """Initiate a chat and process the user prompt.

    Args:
        request (ChatPrompt): Chat prompt data including
        sender ID, conversation ID, and prompt.

    Returns:
        dict: A dictionary containing the user prompt
        and AI-generated response.
    """
    return StreamingResponse(
        process_prompt_stream(
            request.sender_id,
            request.conversation_id,
            CHAT_SYSTEM_PROMPT.format(request.prompt),
        ),
        media_type="text/event-stream",
    )


@router.post("/chat/stream")
def chat_2(request: ChatPrompt):
    """Version 2: [Stream] Initiate a chat and process the user prompt.

    Args:
        request (ChatPrompt): Chat prompt data including sender ID,
        conversation ID, and prompt.

    Returns:
        dict: A dictionary containing the user prompt and
        AI-generated response.
    """
    return StreamingResponse(
        agent_chat(
            agentExecutor, request.prompt, []
        ),
        media_type="text/event-stream",
    )


@router.post("/chat/styled/stream")
async def chat_styled(request: ChatPrompt):
    """Version 2: [Stream] Initiate a chat and process the user prompt.

    Args:
        request (ChatPrompt): Chat prompt data including
        sender ID, conversation ID, and prompt.

    Returns:
        dict: A dictionary containing the user prompt and
        AI-generated response.
    """

    chain = StyleGuide().styleguide_modify_input()

    answer = process_prompt(
        request.sender_id,
        request.conversation_id,
        CHAT_SYSTEM_PROMPT.format(request.prompt),
        use_history=request.use_history,
    )

    def generate(output):
        for chunk in chain.stream({"input": output}):
            yield chunk.content

    return StreamingResponse(
        generate(answer),
        media_type="text/event-stream"
    )


@router.post("/style_engine")
async def style_engine(input_data: Input):
    '''
    Takes in an input text, conforms the text to
    CCL style guide, and streams out the text
    '''

    try:
        # Get the chain from the styleguide_modify_input method
        chain = StyleGuide().styleguide_modify_input()
        
        # Invoke the chain with the provided input data.
        # Assuming that the chain can be called like a function with a dictionary argument
        chain_output = chain.invoke({"input": input_data.input})

        # If chain_output is not in a response-friendly format, convert it to a dict
        response_data = chain_output if isinstance(chain_output, Dict) else chain_output.dict()

        return JSONResponse(content={"result": response_data})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/chat/doc/stream")
async def doc_chat(request: ChatPrompt):
    """Streaming RAG chat
    """
    return StreamingResponse(
        rag_chat(
            request.sender_id,
            request.conversation_id,
            CHAT_SYSTEM_PROMPT.format(request.prompt)
        ),
        media_type="text/event-stream",
    )


@router.post('/test/guard')
def test_guard(request: ChatPrompt):
    return StreamingResponse(
        guardrail_chat(
            request.sender_id,
            request.conversation_id,
            CHAT_SYSTEM_PROMPT.format(request.prompt)
        ),
        media_type="text/event-stream",
    )


@router.post("/upload")
async def upload_files(
    id,
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    """Upload files to an S3 bucket and initiate the
    building of a new index.

    Args:
        id: The folder ID for organizing the files.
        files (list[UploadFile]): List of files to be uploaded.

    Returns:
        JSONResponse: A response containing the list of uploaded files.

    Raises:
        HTTPException: If there is an error during file upload.
        VectorIndexError: If there is an error during index building.
    """
    uploaded_files = []

    try:
        for file in files:
            file_name = file.filename

            # Read the content of the file
            content = await file.read()

            # Upload the file content to S3
            success = bucket_util.upload_file(id, file_name, content)
            if success:
                uploaded_files.append(file.filename)
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to upload file: {file.filename}"
                )
    except Exception as e:
        # Handle errors if needed
        return JSONResponse(content={"error": str(e)}, status_code=500)

    # Start building index
    try:
        print("Building new index...")
        initiate_index(id=id, store_client="chromadb", persist=False)
        print("Index build complete.")
    except Exception as e:
        raise VectorIndexError(e)

    return JSONResponse(
        content={"uploaded_files": uploaded_files},
        status_code=200
    )


@router.get("/user/{user_id}/documents/list")
def list_user_uploaded_docs(user_id):
    """List documents uploaded by a user.

    Args:
        user_id: The ID of the user.

    Returns:
        JSONResponse: A response containing the list of documents.
    """
    docs = bucket_util.list_files_in_folder(user_id)
    return JSONResponse({"docs": docs})


@router.delete("/user/{user_id}/documents")
def delete_all_user_documents(user_id):
    """Delete all documents uploaded by a user.

    Args:
        user_id: The ID of the user.

    Returns:
        JSONResponse: A response indicating the success of the operation.

    Raises:
        HTTPException: If there is an error during deletion.
    """
    try:
        result = bucket_util.delete_from_bucket(user_id)
    except Exception as e:
        return HTTPException(status_code=404, detail=e)
    return JSONResponse({"success": result})


@router.delete("/user/{user_id}/documents/{file_name}")
def delete_user_one_document(user_id, file_name):
    """Delete a specific document uploaded by a user.

    Args:
        user_id: The ID of the user.
        file_name: The name of the file to be deleted.

    Returns:
        JSONResponse: A response indicating the success of the operation.

    Raises:
        HTTPException: If there is an error during deletion.
        VectorIndexError: If there is an error during index building.
    """
    try:
        result = bucket_util.delete_file_in_folder(user_id, file_name)
    except Exception as e:
        return HTTPException(status_code=404, detail=e)

    # Start building index
    try:
        print("Building new index...")
        initiate_index(id=id, persist=False)
        print("Index build complete.")
    except Exception as e:
        raise VectorIndexError(e)

    return JSONResponse({"success": result, "file_name": file_name})


@router.post("/reset-vector-store")
def reindex(buid_index_id: BuildIndexForId):
    """Reset the vector store database.

    Args:
        buid_index_id (BuildIndexForId): Data containing
        the ID for building the index.

    Returns:
        dict: A response indicating the success of the operation.

    Raises:
        VectorIndexError: If there is an error during index building.
    """
    id = buid_index_id.id
    try:
        initiate_index(id=id, store_client="chromadb", persist=False)
    except Exception as e:
        raise VectorIndexError(e)

    return {"message": "Vector store database refreshed!."}


@router.get("/health")
def get_health():
    """Check the health of the system.

    Returns:
        dict: A response indicating the health status.
    """
    return {"message": "Everything is good here 👀"}


@router.get("/NDA/questions")
async def get_nda_questions():
    """Get questions for generating an NDA.

    Returns:
        dict: A response containing the NDA questions.
    """
    return templates.prepare_questions()


@router.post("/NDA/generate")
async def nda_generate(input_data: NDAPrompt):
    """Generate an NDA based on user input.

    Args:
        input_data (NDAPrompt): Input data containing
        answers for generating an NDA.

    Returns:
        JSONResponse: A response containing the generated NDA.

    Raises:
        HTTPException: If there is an error during NDA generation.
    """
    try:
        generator = GenerateNDA(answers=input_data.answers)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    result = generator.handle_sections()
    return JSONResponse(content={"NDA": result})


@router.post("/NDA/generate/stream")
async def nda_generate_2(input_data: NDAPrompt):
    """Version2: [Stream] Generate an NDA based on user input.

    Args:
        input_data (NDAPrompt): Input data containing
        answers for generating an NDA.

    Returns:
        JSONResponse: A response containing the generated NDA.

    Raises:
        HTTPException: If there is an error during NDA generation.
    """
    try:
        generator = GenerateNDA(answers=input_data.answers)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return StreamingResponse(
        generator.handle_sections_2(), media_type="text/event-stream"
    )
