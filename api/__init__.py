from fastapi import FastAPI
from fastapi.responses import JSONResponse
from api.v1.routes import v1
from api.v1.routes.error_handler import (
    AnswersMisMatchQuestion,
    PathTypeMisMatch,
    UnknownSectionID,
    UnknownSectionName,
    UnknownTemplateID,
    VectorIndexError
)


app = FastAPI()

app.include_router(v1.router, prefix="/api/v1")


@app.exception_handler(AnswersMisMatchQuestion)
async def answer_mismatch_question_exception_handler(request, exc):
    return JSONResponse(status_code=404, content={"message": str(exc)})


@app.exception_handler(UnknownSectionName)
async def answer_mismatch_question_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={"message": str(exc)})


@app.exception_handler(UnknownSectionID)
async def answer_mismatch_question_exception_handler(request, exc):
    return JSONResponse(status_code=404, content={"message": str(exc)})


@app.exception_handler(UnknownTemplateID)
async def answer_mismatch_question_exception_handler(request, exc):
    return JSONResponse(status_code=404, content={"message": str(exc)})


@app.exception_handler(PathTypeMisMatch)
async def answer_mismatch_question_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={"message": str(exc)})


@app.exception_handler(VectorIndexError)
async def answer_mismatch_question_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={"message": str(exc)})
