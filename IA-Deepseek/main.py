import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import PyPDF2
from datetime import datetime
import time

# Caminho absoluto para o .env (opcional, mas recomendado)
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)  # Carrega o arquivo .env

# Lê a chave
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

def extract_text_from_pdf(pdf_path):
    """Extrai texto de um arquivo PDF"""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def chat_with_pdf(pdf_path, pdf_text, instructions, model="deepseek-chat", save_txt=False, txt_output_path=None):
    """
    Envia um PDF com instruções para a API do DeepSeek e opcionalmente salva o texto em TXT
    
    Args:
        pdf_path (str): Caminho para o arquivo PDF
        pdf_text (str): Texto extraído do PDF
        instructions (str): Instruções para o processamento do PDF
        model (str): Modelo a ser utilizado
        save_txt (bool): Se True, salva o texto extraído em arquivo TXT
        txt_output_path (str): Caminho para salvar o arquivo TXT. Se None, usa o mesmo nome do PDF com extensão .txt
    
    Returns:
        str: Resposta do modelo
    """
    # Extrai texto do PDF
    
    
    # Salva o texto em arquivo TXT se solicitado
    if save_txt:
        if txt_output_path is None:
            txt_output_path = pdf_path.replace('.pdf', '.txt')
        
        with open(txt_output_path, 'w', encoding='utf-8') as f:
            f.write(pdf_text)
        print(f"Texto do PDF salvo em: {txt_output_path}")
    
    # Prepara a mensagem combinando instruções e conteúdo do PDF
    user_content = f"""
    Siga o modelo abaixo para criar questões dissertativas:
    Ao iniciar a pergunta, coloque "INICIO-" mais o número do descritor (ex: INICIO-D1, INICIO-D2, etc.) para indicar o início da questão.
    1. Descritor: Coloque apenas o número do descritor (ex: D1, D2, etc.)
    2. Questão: Crie uma questão dissertativa com base no descritor.
    3. Alternativas: Crie 5 alternativas, sendo uma correta e quatro incorretas.
    4. Resposta correta: Coloque apenas a letra da alternativa correta (ex: A, B, C, D, E).
    5. Justificativa: Justifique a resposta correta de forma resumida.
    Não coloque nada em negrito ou itálico.
    Ao finalizar a pergunta, coloque "FIM-" mais o número do descritor (ex: FIM-D1, FIM-D2, etc.) para indicar o fim da questão.
    Não coloque mais nenhuma informação além do que foi solicitado.
    O nivel de dificuldade deve ser muito alto.
    {instructions}
    
    Aqui está o conteúdo do documento:
    {pdf_text}
    """
    
    # Faz a requisição para a API
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Você é um assistente especializado em criar questões dissertativas."},
            {"role": "user", "content": user_content}
        ],
        stream=False
    )
    
    return response.choices[0].message.content

def print_and_save_results(pdf_path, pdf_text, instructions_list, output_filename):
    """Processa cada instrução, mostra o progresso e salva os resultados incrementalmente."""
    with open(output_filename, "w", encoding="utf-8") as file:
        file.write(f"=== RELATÓRIO GERADO EM: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n\n")
        
        for idx, instruction in enumerate(instructions_list, start=1):
            start_desc = 5 * (idx - 1) + 1
            end_desc = 5 * idx
            
            print(f"\n[PROCESSANDO] Gerando questões para D{start_desc} a D{end_desc}...")
            start_time = time.time()
            
            result = chat_with_pdf(pdf_path, pdf_text, instruction)
            
            elapsed_time = time.time() - start_time
            print(f"[CONCLUÍDO] Questões D{start_desc}-D{end_desc} prontas. Tempo: {elapsed_time:.2f}s")
            
            # Escreve no arquivo imediatamente (flush garante a escrita física)
            file.write(f"=== DESCRITORES D{start_desc}-D{end_desc} ===\n")
            file.write(result + "\n\n")
            file.flush()  # Força a escrita no disco a cada iteração

if __name__ == "__main__":
    try:
        total_start = time.time()
        print("Iniciando processamento...")
        
        pdf_path = "matriz-de-referencia-de-matematica_2001.pdf"
        pdf_text = """
            **D1** – Identificar figuras semelhantes mediante o reconhecimento de relações de proporcionalidade.
            **D2** – Reconhecer aplicações das relações métricas do triângulo retângulo em um problema que envolva figuras espaciais.
            **D3** – Relacionar diferentes poliedros ou corpos redondos com suas planificações ou vistas.
            **D4** – Identificar a relação entre as representações algébrica e geométrica de um sistema de equações em um problema.
            **D5** – Resolver problema que envolva razões trigonométricas no triângulo retângulo (seno, cosseno, tangente).     
            **D6** – Identificar a localização de pontos no plano cartesiano.
            **D7** – Interpretar geometricamente os coeficientes da equação de uma reta.
            **D8** – Identificar a equação de uma reta apresentada a partir de dois pontos dados ou de um ponto e sua inclinação.
            **D9** – Relacionar a determinação do ponto de interseção de duas ou mais retas com a resolução de um sistema de equações com duas incógnitas.
            **D10** – Reconhecer, entre as equações do 2º grau com duas incógnitas, as que representam circunferências.        
            **D11** – Resolver problema envolvendo o cálculo de perímetro de figuras planas.
            **D12** – Resolver problema envolvendo o cálculo de área de figuras planas.
            **D13** – Resolver problema envolvendo a área total e/ou volume de um sólido (prisma, pirâmide, cilindro, cone, esfera).
            **D14** – Identificar a localização de números reais na reta numérica.
            **D15** – Resolver problema que envolva variação proporcional (direta ou inversa) entre grandezas.
            **D16** – Resolver problema que envolva porcentagem.
            **D17** – Resolver problema envolvendo equação do 2º grau.
            **D18** – Reconhecer expressão algébrica que representa uma função a partir de uma tabela.
            **D19** – Resolver problema envolvendo uma função do 1º grau.
            **D20** – Analisar crescimento/decrescimento, zeros de funções reais apresentadas em gráficos.
            **D21** – Identificar o gráfico que representa uma situação descrita em um texto.
            **D22** – Resolver problema envolvendo P.A./P.G., dada a fórmula do termo geral.
            **D23** – Reconhecer o gráfico de uma função polinomial do 1º grau por meio de seus coeficientes.
            **D24** – Reconhecer a representação algébrica de uma função do 1º grau dado o seu gráfico.
            **D25** – Resolver problemas que envolvam os pontos de máximo ou de mínimo no gráfico de uma função polinomial do 2º grau.
            **D26** – Relacionar as raízes de um polinômio com sua decomposição em fatores do 1º grau.
            **D27** – Identificar a representação algébrica de uma função exponencial a partir de seu gráfico.
            **D28** – Identificar a representação algébrica de uma função logarítmica, reconhecendo-a como inversa da função exponencial.
            **D29** – Resolver problema que envolva função exponencial.
            **D30** – Identificar funções trigonométricas (seno, cosseno, tangente) relacionando-as a suas propriedades.       
            **D31** – Determinar a solução de um sistema linear associando-o a uma representação algébrica ou gráfica.
            **D32** – Resolver problema de contagem utilizando o princípio multiplicativo ou noções de permutação, arranjo ou combinação.
            **D33** – Calcular a probabilidade de um evento.
            **D34** – Resolver problema envolvendo informações apresentadas em tabelas ou gráficos.
            **D35** – Associar informações apresentadas em listas ou tabelas simples aos gráficos que as representam e vice-versa.
        """
        #extract_text_from_pdf(pdf_path)
        
        # Lista de instruções para cada grupo de descritores
        instructions_list = [
            """Crie uma questão dissertativa para os descritores do 3º EM (D1 a D5). 
            5 alternativas, sendo uma correta e quatro incorretas por descritor.""",
            """Crie uma questão dissertativa para os descritores do 3º EM (D6 a D10). 
            5 alternativas, sendo uma correta e quatro incorretas por descritor.""",
            """Crie uma questão dissertativa para os descritores do 3º EM (D11 a D15).
            5 alternativas, sendo uma correta e quatro incorretas por descritor.""",
            """Crie uma questão dissertativa para os descritores do 3º EM (D16 a D20).
            5 alternativas, sendo uma correta e quatro incorretas por descritor.""",
            """Crie uma questão dissertativa para os descritores do 3º EM (D21 a D25).
            5 alternativas, sendo uma correta e quatro incorretas por descritor.""",
            """Crie uma questão dissertativa para os descritores do 3º EM (D26 a D30).
            5 alternativas, sendo uma correta e quatro incorretas por descritor.""",
            """Crie uma questão dissertativa para os descritores do 3º EM (D31 a D35).
            5 alternativas, sendo uma correta e quatro incorretas por descritor.""",
        ]
        
        output_file = f"questoes_EM3_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        print_and_save_results(pdf_path, pdf_text, instructions_list, output_file)
        
        total_time = time.time() - total_start
        print(f"\n✅ Processo finalizado! Tempo total: {total_time:.2f} segundos")
        print(f"📄 Arquivo gerado: {output_file}")
    
    except Exception as e:
        print(f"\n❌ Erro: {e}")