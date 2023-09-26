#!/bin/python3
from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}
