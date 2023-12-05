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
from utilities import (
    FilesDownloadError,
    FolderNotFoundError,
    S3BucketFailToCreateError,
    S3BucketNotFoundError,
)

app = FastAPI(title="CCL Chatbot")
app.include_router(v1.router, prefix="/api/v1")

exception_handlers = {
    AnswersMisMatchQuestion: 422,
    UnknownSectionName: 404,
    UnknownSectionID: 404,
    UnknownTemplateID: 404,
    PathTypeMisMatch: 422,
    VectorIndexError: 404,
    FilesDownloadError: 404,
    FolderNotFoundError: 404,
    S3BucketFailToCreateError: 422,
    S3BucketFailToCreateError: 404
}


for exception, status_code in exception_handlers.items():
    @app.exception_handler(exception)
    async def exception_handler(request, exc):
        return JSONResponse(status_code=status_code, content={"message": str(exc)})
