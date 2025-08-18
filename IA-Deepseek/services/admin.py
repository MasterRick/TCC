from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from create_questions import CreateQuestions

process_status = {"running": False, "current_file": None, "current_difficulty": None}

def process_questions(descriptors_file_name):
    global process_status
    process_status["running"] = True
    for file_name in descriptors_file_name:
        process_status["current_file"] = file_name
        print(f"\nIniciando criação de questões para o arquivo: {file_name}")
        for difficulty in range(3):
            process_status["current_difficulty"] = difficulty
            print(f"Gerando questões com dificuldade {difficulty}...")
            create_questions = CreateQuestions()
            create_questions.create_questions(descriptors_file_name=file_name, difficulty=difficulty)
    process_status["running"] = False
    process_status["current_file"] = None
    process_status["current_difficulty"] = None

def create_questions_service(
    db: Session,
    current_user: dict[str, int],
    background_tasks: BackgroundTasks
):
    if not current_user or not current_user.get("type") == 1:
        raise HTTPException(status_code=403, detail="Acesso negado. Usuário não é administrador.")

    descriptors_file_name = [
        "5ANO_EF_MAT.txt", "9ANO_EF_MAT.txt", "3ANO_EM_MAT.txt",
        "5ANO_EF_POR.txt", "9ANO_EF_POR.txt", "3ANO_EM_POR.txt"
    ]
    
    if process_status["running"]:
        raise HTTPException(status_code=400, detail="Processo de criação de questões já está em execução.")
    else:
        background_tasks.add_task(process_questions, descriptors_file_name)
        return {"detail": "Processo de criação de questões iniciado."}


def get_process_status():
    return process_status