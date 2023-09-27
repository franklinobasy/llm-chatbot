from fastapi import FastAPI
from api.v1.routes import v1


app = FastAPI()

app.include_router(v1.router, prefix="/api/v1")
