from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.descriptor import Descriptor
from models.question import Question

PAGE_SIZE = 20

def get_questions_service(db: Session, page: int = 1, descriptor_id: Optional[int] = None, difficulty: Optional[int] = None, discipline: Optional[str] = None, classroom: Optional[str] = None, year: Optional[str] = None):
    offset = (page - 1) * PAGE_SIZE

    questions = (
        db.query(Question)
        .join(Descriptor)
        .filter(
            (Question.id == descriptor_id) if descriptor_id is not None else True,
            (Question.difficulty == difficulty) if difficulty is not None else True,
            (Descriptor.discipline == discipline) if discipline is not None else True,
            (Descriptor.classroom == classroom) if classroom is not None else True,
            (Descriptor.year == year) if year is not None else True
        )
        .order_by(Question.created_at.desc())
        .offset(offset)
        .limit(PAGE_SIZE)
        .all()
    )

    for question in questions:
        question.content = question_format(question.content)

    return questions

def get_question_service(question_id: int, db: Session):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    question.content = question_format(question.content)
    return question

def question_format(content: str):
    parts = {}

    marks = {
        "FIM-QUESTÃO": "question",
        "FIM-ALTERNATIVAS": "alternatives",
        "FIM-RESPOSTA": "answer",
        "FIM-JUSTIFICATIVA": "justification"
    }

    start = content.find("INICIO") + len("INICIO")
    cursor = start

    for mark, key in marks.items():
        end = content.find(mark)
        parts[key] = content[cursor:end].strip().split(":", 1)[-1].strip()
        cursor = end + len(mark)


    question = parts["question"]
    alternatives_raw = parts["alternatives"]
    answer = parts["answer"]
    justification = parts["justification"]

    return {
        "question": question,
        "alternatives": alternatives_raw,
        "answer": answer,
        "justification": justification
    }
