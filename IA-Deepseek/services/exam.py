
from fastapi import HTTPException       
from sqlalchemy.orm import Session
from sqlalchemy import func
from bodies import exam
from bodies.exam import ExamCreate
from models.descriptor import Descriptor
from models.question import Question
from models.rating import Rating

from services.question import question_format


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
    
    try:
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
            #print(f"Best question ID: {best_question_id} with average rating {rated_questions}")
            best_question = db.query(Question).filter(Question.id == best_question_id).first()
            #print(f"Best question retrieved: ID {best_question.id} with content: {best_question.content}")
            if best_question:
                #print(f"Best question found: ID {best_question.id} with average rating {rated_questions[0][1]}")
                best_question.rating = rated_questions[0][1]  # Adiciona a média de avaliação à questão
                return best_question 
        
        # Se não houver questões avaliadas, retorna uma aleatória
        random_question = (
            db.query(Question)
            .filter(
                Question.descriptor_id == descriptor_id,
                Question.difficulty == difficulty
            )
            .order_by(func.random())
            .first()
        )
        
        if random_question:
            return random_question
        
    except Exception as e:
        return None

def get_all_questions_for_descriptor(db: Session, descriptor_id: int, difficulty: int) -> list[tuple[int, float]]:
    try:
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
        print(f"Rated questions for descriptor {descriptor_id} and difficulty {difficulty}: {rated_questions}")
        return rated_questions
    except Exception as e:
        return None

def get_questions(
    db: Session,
    current_user: dict[str, int],
    desc: str,
    difficulty: int,
    discipline: str,
    classroom: str,
    year: str
):
    exam: list[Question] = []
    descriptors = db.query(Descriptor).filter(
        Descriptor.id == int(desc) if desc.isdigit() else Descriptor.id,
        Descriptor.discipline == discipline,
        Descriptor.classroom == classroom,
        Descriptor.year == year
    ).all()
    
    if not descriptors:
        raise HTTPException(status_code=404, detail="No descriptors found for the given criteria")

    if desc != "all":
        questions = get_all_questions_for_descriptor(db, int(desc), difficulty)
        print(f"Questions retrieved for descriptor {desc} and difficulty {difficulty}: {questions}")
        if not questions:
            raise HTTPException(status_code=404, detail=f"No questions found for descriptor id {desc} with the given difficulty")
        for question_id, avg_rating in questions:
                question = db.query(Question).filter(Question.id == question_id).first()
                if question:
                    question.rating = avg_rating  # Adiciona a média de avaliação à questão
                    question.content = question_format(question.content)
                    exam.append(question)
        
    else:
        for descriptor in descriptors:
            question = get_best_or_random_question(
                db, 
                descriptor.id, 
                difficulty
            )
            if question:
                question.content = question_format(question.content)
                exam.append(question)
            else:
                raise HTTPException(status_code=404, detail=f"No questions found for descriptor id {descriptor.id} with the given difficulty")  
    return  exam