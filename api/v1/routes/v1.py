#!/bin/python3
from fastapi import APIRouter
from bot.bot import get_prompt
from api.v1.models.model import Prompt


router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.post("/send_prompt")
async def receive_prompt(request: Prompt):
    sender_id = request.sender_id
    answer = get_prompt(
        request.sender_id,
        request.prompt,
        use_history=request.use_history
    )

    return {
        'Human': request.prompt,
        'AI': answer
    }
