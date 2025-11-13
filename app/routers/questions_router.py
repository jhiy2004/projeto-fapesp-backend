from fastapi import APIRouter
from app.models.question_models import QuestionID, QuestionResponse
from app.services.questions_service import questions

router = APIRouter(prefix="/questions")

@router.get("/{question_id}", response_model=QuestionResponse)
def answer_question(question_id: QuestionID):
    qid = int(question_id)
    if qid not in questions:
        return {"error": "Invalid question id"}

    entry = questions[qid]
    answer = entry["func"]()

    return {
        "question": entry["text"],
        "answer": answer
    }

