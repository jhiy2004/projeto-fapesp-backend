from enum import Enum
from pydantic import BaseModel

class QuestionID(int, Enum):
    q1 = 1
    q2 = 2
    q3 = 3
    q4 = 4
    q5 = 5
    q6 = 6
    q7 = 7
    q8 = 8

class QuestionResponse(BaseModel):
    question: str
    answer: dict

