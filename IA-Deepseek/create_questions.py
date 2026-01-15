
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
import time
from db import SessionLocal
from models.descriptor import Descriptor
from models.question import Question
import random

class CreateQuestions:
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

    def __init__(self):
        pass

    def _create_question(self, descriptor, difficulty):
        alternate = random.randint(0, 4)
        alternateStr = ""

        if alternate == 0:
            alternateStr = "A"
        elif alternate == 1:
            alternateStr = "B"
        elif alternate == 2:
            alternateStr = "C"
        elif alternate == 3:
            alternateStr = "D"
        elif alternate == 4:
            alternateStr = "E"

        
        db = SessionLocal()
        try:
            user_content = f"""
            Crie uma questão dissertativa para os descritor {descriptor}. 5 alternativas, sendo uma correta e quatro incorretas.
            Dificuldade: {difficulty}, onde 0 é fácil, 1 é médio e 2 é difícil.
            Siga o modelo abaixo para criar questão dissertativa:
            Ao iniciar a questão, coloque "INICIO" para indicar o início da questão.
            1. Questão: Crie uma questão dissertativa com base no descritor.
            FIM-QUESTÃO
            2. Alternativas: Crie as 5 alternativas da questão, sendo uma correta e quatro incorretas.
            A. Alternativa A
            B. Alternativa B
            C. Alternativa C
            D. Alternativa D
            E. Alternativa E
            FIM-ALTERNATIVAS
            3. Resposta correta: Coloque a letra da alternativa correta como {alternateStr}.
            Resposta correta: {alternateStr}
            FIM-RESPOSTA
            4. Justificativa: Justifique a resposta correta de forma resumida.
            Justificativa: A alternativa A é a correta porque...
            FIM-JUSTIFICATIVA
            Não coloque nada em negrito ou itálico.
            Ao finalizar a questão, coloque "FIM" para indicar o fim da questão.
            Não coloque mais nenhuma informação além do que foi solicitado.
            """

            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "Você é um assistente especializado em criar questões dissertativas."},
                    {"role": "user", "content": user_content}
                ],
                stream=False
            )
            
            descriptor_data = {
                "name": descriptor.split("–")[0].strip(),
                "content": descriptor.split("–")[1].strip(),
            }

            descriptor = db.query(Descriptor).filter(Descriptor.name == descriptor_data["name"], Descriptor.content == descriptor_data["content"]).first()
            print(f"Descritor: {descriptor}")

            if not descriptor:
                raise Exception(f"Erro ao buscar descritor: {descriptor_data}")

            question = Question(
                descriptor=descriptor,
                difficulty=difficulty,
                source="DeepSeek",
                content=response.choices[0].message.content
            )
            db.add(question)
            db.commit()
            db.refresh(question) 

            return question
       
        except Exception as e:
            print(f"Erro ao criar questão: {e}")
            return None
       

    def print_and_save_results(self, descriptor_list = [], difficulty=0):
        try:
                for index, descriptor in enumerate(descriptor_list, start=0):
                    print(f"\n[PROCESSANDO] Gerando questão para o {descriptor}")
                    start_time = time.time()
                    self._create_question(descriptor, difficulty)
                    elapsed_time = time.time() - start_time
                    print(f"[CONCLUÍDO] Questão para o {descriptor} gerada em {elapsed_time:.2f} segundos.")  
        except Exception as e:
            print(f"Erro ao processar o descritor: {e}")

    def create_questions(self, total_start = time.time(), descriptors_file_name = "3ANO_EM_MAT.txt", difficulty=0):
        try:
            try:
                print("Iniciando processamento...")
                create_questions = CreateQuestions()
                descriptor_list = []

                print(f"📄 Carregando arquivo de descritores: {descriptors_file_name}")
                with open(Path(f"Material de Referencia/Descritores/{descriptors_file_name}"), "r", encoding="utf-8") as f:
                    descriptor_list = f.readlines()
                print(f"📄 {len(descriptor_list)} descritores carregados com sucesso!")
            except Exception as e:
                print(f"\n❌ Erro de processamento: {e}")

            try:
                create_questions.print_and_save_results(descriptor_list, difficulty=difficulty)

                total_time = time.time() - total_start
                print(f"\n✅ Processo finalizado! Tempo total: {total_time:.2f} segundos")

            except Exception as e:
                print(f"\n❌ Erro de Criação: {e}")
        except asyncio.CancelledError:
            print("\n❌ Processo cancelado pelo usuário.")

if __name__ == "__main__":
    descriptors_file_name = ["9ANO_EF_MAT.txt", "5ANO_EF_POR.txt", "9ANO_EF_POR.txt", "3ANO_EM_POR.txt"]
    create_questions = CreateQuestions()

    for i in range(1):
        for file_name in descriptors_file_name:
            print(f"\nIniciando criação de questões para o arquivo: {file_name}")
            for difficulty in range(3):
                print(f"Gerando questões com dificuldade {difficulty}...")
                create_questions.create_questions(descriptors_file_name=file_name, difficulty=difficulty)
        


