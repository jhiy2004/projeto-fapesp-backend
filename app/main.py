from fastapi import FastAPI
from app.routers.questions_router import router as questions_router
from app.routers.predict_router import router as predict_router

app = FastAPI()

@app.get("/")
def read_root():
    return { "Hello": "World" }

app.include_router(questions_router)
app.include_router(predict_router)