from fastapi import FastAPI
from app.routers.questions_router import router as questions_router

app = FastAPI()

@app.get("/")
def read_root():
    return { "Hello": "World" }

app.include_router(questions_router)
