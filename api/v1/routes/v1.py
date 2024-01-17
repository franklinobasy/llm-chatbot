#!/bin/python3
import os
from typing import Annotated
from fastapi import (
    File,
    UploadFile,
    APIRouter,
    HTTPException,
)
from fastapi.responses import JSONResponse, StreamingResponse

from api.v1.models.models import (
    BuildIndexForId,
    ChatPrompt,
    Input,
    LetterContext,
    LetterResult,
    NDAPrompt,
    ProposalResult,
    Questions,
    Sections,
    Templates,
    UserInput,
    UploadRequestModel,
    UserInput2,
)
from api.v1.routes.error_handler import (
    AnswersMisMatchQuestion,
    PathTypeMisMatch,
    UnknownSectionID,
    UnknownSectionName,
    UnknownTemplateID,
    VectorIndexError,
)
from chatbot_v2.ai.chat import process_prompt, process_prompt_2
from chatbot_v2.ai.generate_proposal import AutoFillTemplate
from chatbot_v2.ai.generate_letter import AutoWriteLetter
from chatbot_v2.ai.generate_nda import GenerateNDA, templates
from chatbot_v2.ai.generate_proposal_2 import AutoGenerateSection
from chatbot_v2.ai.style_engine import StyleGuide
from chatbot_v2.configs.constants import MODEL_NAME
from chatbot_v2.handlers.field_handler import FieldHandler
from chatbot_v2.handlers.question_handler import QuestionHandler
from chatbot_v2.handlers.template_handler import TemplateHandler
from chatbot_v2.vector_store.index import initiate_index
from chatbot_v2.templates.templates import section_templates
from chatbot_v2.templates.context_config import (
    CHAT_SYSTEM_PROMPT,
)
from database.mongodb.tools import (
    delete_conversation,
    get_user_conversations,
    get_prompts_from_conversation,
    create_conversation
)
from utilities.aws_tools import BucketUtil
from uuid import uuid4

router = APIRouter()
bucket_util = BucketUtil(bucket_name="ccl-chatbot-document-store")


@router.get("/sections")
async def get_all_sections():
    """Get all available sections.

    Returns:
        Sections: A response containing a list of available sections.
    """ 
    return Sections(sections=list(section_templates.keys()))


@router.get("/questions/{section_id}")
async def get_section_questions(section_id: int):
    """Get questions for a specific section.

    Args:
        section_id (int): The ID of the section.

    Returns:
        Questions: A response containing the section name and a list of questions.
    
    Raises:
        PathTypeMisMatch: If the provided section ID is not an integer.
        UnknownSectionID: If the section ID is out of range.
    """
    if not isinstance(section_id, int):
        raise PathTypeMisMatch(section_id)

    try:
        section_name = list(section_templates.keys())[section_id]
        section = QuestionHandler(section_name)
        questions = section.get_questions()
        return Questions(section_name=section_name, questions=questions)
    except IndexError:
        raise UnknownSectionID(section_id)


@router.get("/templates/{section_id}")
async def get_section_templates(section_id: int):
    """Get templates for a specific section.

    Args:
        section_id (int): The ID of the section.

    Returns:
        Templates: A response containing the section name and a list of templates.
    
    Raises:
        PathTypeMisMatch: If the provided section ID is not an integer.
        UnknownSectionID: If the section ID is out of range.
    """
    if not isinstance(section_id, int):
        raise PathTypeMisMatch(section_id)

    try:
        section_name = list(section_templates.keys())[section_id]
        template_store = TemplateHandler(section_name)
        templates = template_store.get_templates()
        return Templates(section_name=section_name, templates=templates)
    except IndexError:
        raise UnknownSectionID(section_id)


@router.post("/generate")
async def generate_proposal(user_input: UserInput):
    """Generate a proposal based on user input.

    Args:
        user_input (UserInput): User input data including section ID, template index, and answers.

    Returns:
        ProposalResult: A response containing the generated proposal text.
    
    Raises:
        UnknownSectionID: If the section ID is out of range.
        UnknownTemplateID: If the template index is out of range.
        AnswersMisMatchQuestion: If the number of answers does not match the number of questions.
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
            n_questions=len(question_handler.get_questions()), n_answers=len(answers)
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


@router.post('/generate/proposal')
async def generate_proposal(user_input: UserInput2):
    """ Version 2: Generate a proposal section """
    section_id = user_input.section_id
    template_index = user_input.template_index
    context = user_input.context
    
    try:
        section_name = list(section_templates.keys())[section_id]
    except IndexError as _:
        raise UnknownSectionID(section_id)
    
    generator = AutoGenerateSection(MODEL_NAME, section_name)
    
    # prepare template
    generator.section_template(template_index)
    
    # prepare questions
    generator.template_questions()
    
    result = generator.generate_section(context)
    return result


@router.post('/generate/proposal/stream')
async def generate_proposal_2(user_input: UserInput2):
    """ Version 2: [Stream] Generate a proposal section """
    section_id = user_input.section_id
    template_index = user_input.template_index
    context = user_input.context
    
    try:
        section_name = list(section_templates.keys())[section_id]
    except IndexError as _:
        raise UnknownSectionID(section_id)
    
    generator = AutoGenerateSection(MODEL_NAME, section_name)
    
    # prepare template
    try:
        generator.section_template(template_index)
    except IndexError as _:
        raise UnknownSectionID(section_id)
    
    if section_name in generator.no_llm_sections:
        return StreamingResponse(
            generator.stream_section_generation(chunk_size=100),
            media_type='text/event-stream'
        )
    
    # prepare questions
    generator.template_questions()
    
    return StreamingResponse(
        generator.generate_section_2(context),
        media_type='text/event-stream'
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
        media_type='text/event-stream'
    )


@router.post("/chat")
async def chat(request: ChatPrompt):
    """Initiate a chat and process the user prompt.

    Args:
        request (ChatPrompt): Chat prompt data including sender ID, conversation ID, and prompt.

    Returns:
        dict: A dictionary containing the user prompt and AI-generated response.
    """
    answer = process_prompt(
        request.sender_id,
        request.conversation_id,
        CHAT_SYSTEM_PROMPT.format(request.prompt),
        use_history=request.use_history,
    )

    return {"Human": request.prompt, "AI": answer}


@router.post("/chat/stream")
async def chat_2(request: ChatPrompt):
    """Version 2: [Stream] Initiate a chat and process the user prompt.

    Args:
        request (ChatPrompt): Chat prompt data including sender ID, conversation ID, and prompt.

    Returns:
        dict: A dictionary containing the user prompt and AI-generated response.
    """
    return StreamingResponse(
        process_prompt_2(
            request.sender_id,
            request.conversation_id,
            CHAT_SYSTEM_PROMPT.format(request.prompt),
            use_history=request.use_history,
        ),
        media_type='text/event-stream'
    )


@router.post("/upload")
async def upload_files(
    id,
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    """Upload files to an S3 bucket and initiate the building of a new index.

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
                    status_code=500, detail=f"Failed to upload file: {file.filename}"
                )
    except Exception as e:
        # Handle errors if needed
        return JSONResponse(content={"error": str(e)}, status_code=500)

    # Start building index
    try:
        print("Building new index...")
        initiate_index(id=id, persist=False)
        print("Index build complete.")
    except Exception as e:
        raise VectorIndexError(e)

    return JSONResponse(content={"uploaded_files": uploaded_files}, status_code=200)


@router.get('/user/{user_id}/documents/list')
def list_user_uploaded_docs(user_id):
    """List documents uploaded by a user.

    Args:
        user_id: The ID of the user.

    Returns:
        JSONResponse: A response containing the list of documents.
    """
    docs = bucket_util.list_files_in_folder(user_id)
    return JSONResponse({
        "docs": docs
    })


@router.delete('/user/{user_id}/documents')
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
        return HTTPException(
            status_code=404,
            detail=e
        )
    return JSONResponse(
        {
            'success': result
        }
    )


@router.delete('/user/{user_id}/documents/{file_name}')
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
        return HTTPException(
            status_code=404,
            detail=e
        )
    
    # Start building index
    try:
        print("Building new index...")
        initiate_index(id=id, persist=False)
        print("Index build complete.")
    except Exception as e:
        raise VectorIndexError(e)
    
    return JSONResponse(
        {
            'success': result,
            'file_name': file_name
        }
    )


@router.post("/reset-vector-store")
def reindex(buid_index_id: BuildIndexForId):
    """Reset the vector store database.

    Args:
        buid_index_id (BuildIndexForId): Data containing the ID for building the index.

    Returns:
        dict: A response indicating the success of the operation.
    
    Raises:
        VectorIndexError: If there is an error during index building.
    """
    id = buid_index_id.id
    try:
        initiate_index(id=id, persist=False)
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


# @router.post("/style_engine")
# async def style_playground_endpoint(input_data: Input):
#     """Modify the input using the style engine.

#     Args:
#         input_data (Input): Input data to be modified.

#     Returns:
#         JSONResponse: A response containing the modified result.
    
#     Raises:
#         HTTPException: If there is an error during modification.
#     """
#     try:
#         style_guide = StyleGuide()
#         chain = style_guide.styleguide_modify_input()
#         chain_output = chain.invoke({"input": input_data.input})
#         response_data = (
#             chain_output if isinstance(chain_output, dict) else chain_output.dict()
#         )
#         return JSONResponse(content={"result": response_data})
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


@router.get('/conversations/user/{user_id}')
async def get_user_conversations_(user_id):
    """Get conversations for a specific user.

    Args:
        user_id: The ID of the user.

    Returns:
        dict: A response containing the user's conversations.
    """
    conversations = get_user_conversations(user_id)
    return conversations


@router.get('/converstion/prompts/user/{user_id}/{conversation_id}')
async def get_prompts_from_conversation_(user_id, conversation_id):
    """Get prompts from a specific conversation.

    Args:
        user_id: The ID of the user.
        conversation_id: The ID of the conversation.

    Returns:
        dict: A response containing the prompts from the conversation.
    """
    prompts = get_prompts_from_conversation(
        user_id, conversation_id
    )
    return prompts


@router.get('/conversation/create/{user_id}')
def create_new_conversation(user_id):
    """Create a new conversation for a user.

    Args:
        user_id: The ID of the user.

    Returns:
        dict: A response containing the ID of the new conversation.
    """
    conversation_id = create_conversation(user_id)
    return conversation_id


@router.delete('/conversation/delete/{user_id}/{conversation_id}')
def delete_user_conversation(user_id, conversation_id):
    """Delete a conversation for a specific user.

    Args:
        user_id: The ID of the user.
        conversation_id: The ID of the conversation.

    Returns:
        dict: A response indicating the success of the operation.
    """
    return delete_conversation(user_id, conversation_id)


@router.get('/NDA/questions')
async def get_nda_questions():
    """Get questions for generating an NDA.

    Returns:
        dict: A response containing the NDA questions.
    """
    return templates.prepare_questions()


@router.post('/NDA/generate')
async def nda_generate(input_data: NDAPrompt):
    """Generate an NDA based on user input.

    Args:
        input_data (NDAPrompt): Input data containing answers for generating an NDA.

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
    return JSONResponse(
        content={
            "NDA": result
        }
    )


@router.post('/NDA/generate/stream')
async def nda_generate_2(input_data: NDAPrompt):
    """Version2: [Stream] Generate an NDA based on user input.

    Args:
        input_data (NDAPrompt): Input data containing answers for generating an NDA.

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
        generator.handle_sections_2(),
        media_type='text/event-stream'
    )
