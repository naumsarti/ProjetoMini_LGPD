from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, DateTime, insert, text
from datetime import datetime
import os
import csv
import time
from functools import wraps

#Atividade 4
def medir_tempo(func):
    """Decorator que mede o tempo de execução de uma função."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()  # tempo inicial (mais preciso que time.time)
        resultado = func(*args, **kwargs)
        fim = time.perf_counter()     # tempo final
        duracao = fim - inicio

        mensagem_log = f"[{datetime.now()}] Função '{func.__name__}' executada em {duracao:.6f} segundos.\n"
        with open("execucao.log", "a", encoding="utf-8") as f:
            f.write(mensagem_log)

        print(f"⏱ Log gravado '{func.__name__}' finalizada em {duracao:.6f}s")
        return resultado
    return wrapper

engine = create_engine("postgresql+psycopg2://alunos:AlunoFatec@200.19.224.150:5432/atividade2", echo=False)
metadata = MetaData()

usuarios = Table(
    'usuarios', metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String(50), nullable=False, index=True),
    Column('cpf', String(14), nullable=False),
    Column('email', String(100), nullable=False, unique=True),
    Column('telefone', String(20), nullable=False),
    Column('data_nascimento', Date, nullable=False),
    Column('created_on', DateTime(), default=datetime.now),
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
)

metadata.create_all(engine)

# Atividade 1
def LGPD(row): 
    dado = dict(row._mapping)
    
    partes_nome = dado['nome'].split(' ', 1)
    primeiro_nome = partes_nome[0]
    sobrenome = partes_nome[1] if len(partes_nome) > 1 else ""
    dado['nome'] = primeiro_nome[0] + ("*" * (len(primeiro_nome) - 1)) + (" " + sobrenome if sobrenome else "")

    dado['cpf'] = f"{dado['cpf'][:3]}.***.***-**"

    usuario, dominio = dado['email'].split('@')
    dado['email'] = usuario[0] + ("*" * (len(usuario) - 1)) + "@" + dominio

    dado['telefone'] = dado['telefone'][-4:]

    return dado

# Atividade 2
@medir_tempo
def gerar_csv_por_ano():
    pasta_destino = "registros_anos"   
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
        print(f"Pasta '{pasta_destino}' criada.")

    dados_agrupados = {}
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM usuarios;"))
        for row in result:
            dado_anonimo = LGPD(row)
            ano = dado_anonimo['data_nascimento'].year
            if ano not in dados_agrupados:
                dados_agrupados[ano] = []
            dados_agrupados[ano].append(dado_anonimo)

    for ano, registros in dados_agrupados.items():
        caminho_arquivo = os.path.join(pasta_destino, f"{ano}.csv")
        with open(caminho_arquivo, "w", newline="", encoding="utf-8") as f:
            if registros:
                escritor = csv.DictWriter(f, fieldnames=registros[0].keys())
                escritor.writeheader()
                escritor.writerows(registros)
        
    print(f"\nProcesso concluído! {len(dados_agrupados)} arquivos gerados em '{pasta_destino}'.")

# Atividade 3
@medir_tempo
def gerar_csv_todos():
    nome_arquivo = "todos.csv"
    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT nome, cpf FROM usuarios;"))
        
        with open(nome_arquivo, "w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(['nome', 'cpf'])
            
            for row in result:
                escritor.writerow([row.nome, row.cpf])
                
    print(f"\nArquivo '{nome_arquivo}' gerado com sucesso contendo todos os registros.")

users = []
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM usuarios LIMIT 5;"))
    for row in result:
        row = LGPD(row)
        users.append(row)

for user in users:
    print(user)

if __name__ == "__main__":
    gerar_csv_por_ano()
    gerar_csv_todos()