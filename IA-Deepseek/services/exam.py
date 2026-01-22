
from http.client import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from bodies import exam
from bodies.exam import ExamCreate
from models.descriptor import Descriptor
from models.question import Question
from models.rating import Rating
import random


def get_best_or_random_question(db: Session, descriptor_id: int, difficulty: int):
    """
    Busca a questão com melhor avaliação média de um descritor.
    Se não houver questões avaliadas, retorna uma aleatória.
    
    Critérios de avaliação:
    - coherence (Coerência)
    - contextualization (Contextualização)
    - difficulty_level (Nível de dificuldade)
    - clarity (Clareza)
    - descriptor_alignment (Alinhamento com descritor)
    """
    
    # Calcular média das avaliações por questão
    rated_questions = (
        db.query(
            Question.id,
            func.avg((
                Rating.coherence + 
                Rating.contextualization + 
                Rating.difficulty_level + 
                Rating.clarity + 
                Rating.descriptor_alignment
            ) / 5).label('avg_rating')
        )
        .outerjoin(Rating, Question.id == Rating.question_id)
        .filter(
            Question.descriptor_id == descriptor_id,
            Question.difficulty == difficulty
        )
        .group_by(Question.id)
        .order_by(func.avg((
            Rating.coherence + 
            Rating.contextualization + 
            Rating.difficulty_level + 
            Rating.clarity + 
            Rating.descriptor_alignment
        ) / 5).desc())
        .all()
    )
    
    if rated_questions:
        # Retorna a questão com melhor avaliação
        best_question_id = rated_questions[0][0]
        return db.query(Question).filter(Question.id == best_question_id).first()
    
    # Se não houver questões avaliadas, retorna uma aleatória
    random_question = (
        db.query(Question)
        .filter(
            Question.descriptor_id == descriptor_id,
            Question.difficulty == difficulty
        )
        .all()
    )
    
    if random_question:
        return random.choice(random_question)
    
    return None


def create_exam_service(
    db: Session,
    current_user: dict[str, int],
    created_exam: ExamCreate
):
    exam = []
    if created_exam.questions:
        for q_id in created_exam.questions:
            question = db.query(Question).filter(Question.id == q_id).first()
            exam.append(question)
            if not question:
                raise HTTPException(status_code=404, detail=f"Question with id {q_id} not found")
    else:
        descriptors = db.query(Descriptor).filter(
            Descriptor.discipline == created_exam.discipline,
            Descriptor.classroom == created_exam.classroom,
            Descriptor.year == created_exam.year
        ).all()
        
        if not descriptors:
            raise HTTPException(status_code=404, detail="No descriptors found for the given criteria")

        for descriptor in descriptors:
            question = get_best_or_random_question(
                db, 
                descriptor.id, 
                created_exam.difficulty
            )
            if question:
                exam.append(question)
            else:
                raise HTTPException(status_code=404, detail=f"No questions found for descriptor id {descriptor.id} with the given difficulty")
        
            
    return {"message": "Exam created successfully", "exam": exam}