#!/bin/python3
import os
from typing import Annotated
from fastapi import (
    File,
    UploadFile,
    APIRouter,
    HTTPException,
)

from fastapi.responses import JSONResponse


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
)
from api.v1.routes.error_handler import (
    AnswersMisMatchQuestion,
    PathTypeMisMatch,
    UnknownSectionID,
    UnknownSectionName,
    UnknownTemplateID,
    VectorIndexError,
)
from chatbot_v2.ai.chat import process_prompt
from chatbot_v2.ai.generate_proposal import AutoFillTemplate
from chatbot_v2.ai.generate_letter import AutoWriteLetter
from chatbot_v2.ai.generate_nda import GenerateNDA, templates
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
    return Sections(sections=list(section_templates.keys()))


@router.get("/questions/{section_id}")
async def get_section_questions(section_id: int):
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

    # # Get all the fiels in the selected template
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


@router.post("/letter")
def write_letter(letter_context: LetterContext):
    context = letter_context.context
    llm = AutoWriteLetter(MODEL_NAME)
    generated_letter = llm.generate(context)
    return LetterResult(text=generated_letter)


@router.post("/chat")
async def chat(request: ChatPrompt):
    answer = process_prompt(
        request.sender_id,
        request.conversation_id,
        CHAT_SYSTEM_PROMPT.format(request.prompt),
        use_history=request.use_history,
    )

    return {"Human": request.prompt, "AI": answer}


@router.post("/upload")
async def upload_files(
    id,
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    uploaded_files = []

    try:
        for file in files:
            # Upload the file directly to S3
            ext = file.filename.split(".").pop()
            # Generate a unique filename
            file_name = f"{uuid4().hex}.{ext}"

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


@router.post("/reset-vector-store")
def reindex(buid_index_id: BuildIndexForId):
    id = buid_index_id.id
    try:
        initiate_index(id=id, persist=False)
    except Exception as e:
        raise VectorIndexError(e)

    return {"message": "Vector store database refreshed!."}


@router.get("/health")
def get_health():
    return {"message": "Everything is good here 👀"}


@router.post("/style_engine")
async def style_playground_endpoint(input_data: Input):
    try:
        style_guide = StyleGuide()
        chain = style_guide.styleguide_modify_input()
        chain_output = chain.invoke({"input": input_data.input})
        response_data = (
            chain_output if isinstance(chain_output, dict) else chain_output.dict()
        )
        return JSONResponse(content={"result": response_data})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/conversations/user/{user_id}')
async def get_user_conversations_(user_id):
    conversations = get_user_conversations(user_id)
    return conversations


@router.get('/converstion/prompts/user/{user_id}/{conversation_id}')
async def get_prompts_from_conversation_(user_id, conversation_id):
    prompts = get_prompts_from_conversation(
        user_id, conversation_id
    )
    return prompts


@router.get('/conversation/create/{user_id}')
def create_new_conversation(user_id):
    conversation_id = create_conversation(user_id)
    return conversation_id


@router.get('/NDA/questions')
async def get_nda_questions():
    return templates.prepare_questions()


@router.post('/NDA/generate')
async def nda_generate(input_data: NDAPrompt):
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
