
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
import time

from requests import session
from db import Base, engine,SessionLocal
from models.descriptor import Descriptor
from models.question import Question

class CreateQuestions:
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

    def __init__(self):
        pass

    def _create_question(self, descriptor, difficulty):
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
        try:
            user_content = f"""
            Crie uma questão dissertativa para os descritor {descriptor}. 5 alternativas, sendo uma correta e quatro incorretas.
            Dificuldade: {difficulty}, onde 0 é fácil, 1 é médio e 2 é difícil.
            Siga o modelo abaixo para criar questão dissertativa:
            Ao iniciar a questão, coloque "INICIO-" mais o número do descritor (ex: INICIO-D1, INICIO-D2, etc.) para indicar o início da questão.
            1. Descritor: Coloque apenas o número do descritor (ex: D1, D2, etc.)
            2. Questão: Crie uma questão dissertativa com base no descritor.
            3. Alternativas: Crie 5 alternativas, sendo uma correta e quatro incorretas.
            4. Resposta correta: Coloque apenas a letra da alternativa correta (ex: A, B, C, D, E).
            5. Justificativa: Justifique a resposta correta de forma resumida.
            Não coloque nada em negrito ou itálico.
            Ao finalizar a questão, coloque "FIM-" mais o número do descritor (ex: FIM-D1, FIM-D2, etc.) para indicar o fim da questão.
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
                "name": descriptor.split("–")[0],
                "content": descriptor.split("–")[1],
            }

            descriptor = db.query(Descriptor).filter(Descriptor.name == descriptor_data["name"] and Descriptor.content == descriptor_data["content"]).first()
            print(f"Descriptor encontrado: {descriptor}")
            question = Question(
                descriptor=descriptor,
                difficulty=difficulty,
                content=response.choices[0].message.content
            )
            db.add(question)
            db.commit()
            db.refresh(question) 

            return question
       
        except Exception as e:
            print(f"Erro ao criar questão: {e}")
            return None
       

    def print_and_save_results(self, descriptor_list = []):
        try:
                for index, descriptor in enumerate(descriptor_list, start=1):
                    print(f"\n[PROCESSANDO] Gerando questão para o {descriptor}")
                    start_time = time.time()
                    self._create_question(descriptor, 1)
                    elapsed_time = time.time() - start_time
                    print(f"[CONCLUÍDO] Questão para o {descriptor} gerada em {elapsed_time:.2f} segundos.")  
        except Exception as e:
            print(f"Erro ao processar o descritor: {e}")

    def create_questions(self, total_start = time.time(), descriptors_file_name = "3ANO_EM_MAT.txt"):
        try:
            try:
                print("Iniciando processamento...")
                now = datetime.now()
                formatted = now.strftime('%Y-%m-%d_%H%M%S') + f'{int(now.microsecond / 1000):03d}'
                output_file = f"{formatted}_{descriptors_file_name.split('.')[0]}_questoes.txt"
                create_questions = CreateQuestions()
                descriptor_list = []

                print(f"📄 Carregando arquivo de descritores: {descriptors_file_name}")
                with open(Path(f"Material de Referencia/Descritores/{descriptors_file_name}"), "r", encoding="utf-8") as f:
                    descriptor_list = f.readlines()
                print(f"📄 {len(descriptor_list)} descritores carregados com sucesso!")
            except Exception as e:
                print(f"\n❌ Erro de processamento: {e}")

            try:
                create_questions.print_and_save_results(descriptor_list)

                total_time = time.time() - total_start
                print(f"\n✅ Processo finalizado! Tempo total: {total_time:.2f} segundos")
                print(f"📄 Arquivo gerado: {output_file}")

            except Exception as e:
                print(f"\n❌ Erro de Criação: {e}")
        except asyncio.CancelledError:
            print("\n❌ Processo cancelado pelo usuário.")


