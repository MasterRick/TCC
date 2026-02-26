from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from bodies.question import QuestionByFileCreate, QuestionCreate
from models.descriptor import Descriptor
from models.question import Question
from models.rating import Rating
from create_questions import CreateQuestions
from fastapi import BackgroundTasks
from db import get_db

PAGE_SIZE = 20


def _average_rating_expression():
    return (
        Rating.coherence
        + Rating.contextualization
        + Rating.difficulty_level
        + Rating.clarity
        + Rating.descriptor_alignment
    ) / 5


def _attach_average_ratings(db: Session, questions: list[Question]):
    if not questions:
        return

    question_ids = [question.id for question in questions]

    rating_rows = (
        db.query(
            Rating.question_id,
            func.avg(_average_rating_expression()).label("avg_rating")
        )
        .filter(Rating.question_id.in_(question_ids))
        .group_by(Rating.question_id)
        .all()
    )

    ratings_by_question_id = {question_id: avg_rating for question_id, avg_rating in rating_rows}

    for question in questions:
        avg_rating = ratings_by_question_id.get(question.id)
        question.rating = float(avg_rating) if avg_rating is not None else None

def get_questions_service(
    db: Session,
    user_id: int,
    page: int = 1,
    descriptor_id: Optional[int] = None,
    difficulty: Optional[int] = None,
    discipline: Optional[str] = None,
    classroom: Optional[str] = None,
    year: Optional[str] = None
):
    offset = (page - 1) * PAGE_SIZE

    query = (
        db.query(Question)
        .join(Descriptor)
        .outerjoin(Rating, (Rating.question_id == Question.id) & (Rating.user_id == user_id))
        .filter(Rating.id.is_(None)) 
    )

    if descriptor_id is not None:
        query = query.filter(Descriptor.id == descriptor_id)
    if difficulty is not None:
        query = query.filter(Question.difficulty == difficulty)
    if discipline is not None:
        query = query.filter(Descriptor.discipline == discipline)
    if classroom is not None:
        query = query.filter(Descriptor.classroom == classroom)
    if year is not None:
        query = query.filter(Descriptor.year == year)

    questions = (
        query.order_by(Question.created_at.desc())
        .offset(offset)
        .limit(PAGE_SIZE)
        .all()
    )

    for question in questions:
        question.content = question_format(question.content)

    _attach_average_ratings(db, questions)

    return questions

def get_question_service(question_id: int, db: Session):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    average_rating = (
        db.query(func.avg(_average_rating_expression()))
        .filter(Rating.question_id == question.id)
        .scalar()
    )

    question.rating = float(average_rating) if average_rating is not None else None
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

process_status = {"running": False, "current_file": None, "current_difficulty": None, "current_descriptor": None, "current_content": None}

def process_questions(descriptors_file_name, difficulty, content):
    global process_status
    process_status["running"] = True
    try:
        #for file_name in descriptors_file_name:
            process_status["current_file"] = descriptors_file_name
            print(f"\nIniciando criação de questões para o arquivo: {descriptors_file_name}")
            #for difficulty in range(3):
            process_status["current_difficulty"] = difficulty
            process_status["current_content"] = content
            print(f"Gerando questões com dificuldade {difficulty}...")
            create_questions = CreateQuestions()
            create_questions.create_questions(descriptors_file_name=descriptors_file_name, difficulty=difficulty, content=content)
    finally:
        process_status["running"] = False
        process_status["current_file"] = None
        process_status["current_difficulty"] = None
        process_status["current_content"] = None

def process_question(descriptor_id: int, difficulty: int, content: str):
    global process_status
    process_status["running"] = True
    try:
        process_status["current_file"] = "Single Question"
        process_status["current_difficulty"] = difficulty
        process_status["current_descriptor"] = descriptor_id
        process_status["current_content"] = content

        print(f"\nIniciando criação de questão para o descritor: {descriptor_id} com dificuldade {difficulty}")
    
        create_questions = CreateQuestions()
        create_questions.create_question(descriptor_id, difficulty, content)

    finally:
        process_status["running"] = False
        process_status["current_file"] = None
        process_status["current_difficulty"] = None
        process_status["current_descriptor"] = None
        process_status["current_content"] = None

def create_questions_service(
    db: Session,
    current_user: dict[str, int],
    background_tasks: BackgroundTasks,
    question_info: QuestionByFileCreate
):
    print(current_user)
    if current_user.get("type") != 1:
        raise HTTPException(status_code=403, detail="Acesso negado. Usuário não é administrador.")

    #descriptors_file_name = [
    #    "5ANO_EF_MAT.txt", "9ANO_EF_MAT.txt", "3ANO_EM_MAT.txt",
    #    "5ANO_EF_POR.txt", "9ANO_EF_POR.txt", "3ANO_EM_POR.txt"
    #]

    print(f"Recebido pedido de criação de questões para disciplina {question_info.discipline}, sala {question_info.classroom}, ano {question_info.year} e dificuldade {question_info.difficulty}")
    
    if process_status["running"]:
        raise HTTPException(status_code=400, detail="Processo de criação de questões já está em execução.")
    else:
        background_tasks.add_task(process_questions, f"{question_info.year}_{question_info.classroom}_{question_info.discipline}.txt", question_info.difficulty, question_info.content)
        return {"detail": "Processo de criação de questões iniciado."}

def create_questions_service_single(
    question_info:QuestionCreate,
    background_tasks: BackgroundTasks,
):
     if process_status["running"]:
        raise HTTPException(status_code=400, detail="Processo de criação de questões já está em execução.")
     else:
        background_tasks.add_task(process_question, question_info.descriptor_id, question_info.difficulty, question_info.content)
        return {"detail": "Processo de criação de questão iniciado."}

def get_process_status():
    return process_status