# Mini Projeto LGPD - Fatec Rio Claro
Este repositório contém a implementação de um **Mini Projeto de LGPD**. O projeto demonstra a manipulação de dados sensíveis extraídos de um banco de dados PostgreSQL através de técnicas de anonimização e geração de logs.

> *Projeto desenvolvido para fins acadêmicos na Fatec Rio Claro.*

## Tecnologias Utilizadas

* **Python 3.13** 
* **SQLAlchemy:** Para a orquestração e conexão ao banco de dados PostgreSQL.
* **Psycopg2:** Driver de conexão ao PostgreSQL.
* **CSV & OS:** Bibliotecas nativas para manipulação de arquivos e diretórios.

## Como Rodar

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/naumsarti/ProjetoMini_LGPD.git
    cd ProjetoMini_LGPD
    ```

2.  **Crie um Ambiente Virtual:**
    - **Windows**
    ```bash
    python -m venv .venv
    .venv/Scripts/activate
    ```
    - **Linux/macOS**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
    
3.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuração do Banco de Dados:**
    > As credenciais de acesso utilizadas no projeto seguem o padrão estabelecido pela instituição.

5.  **Execute o script:**
    ```bash
    python LGPD.py
    ```

