# Employee Manager | InNovaIdeia

**Sistema de gestão de funcionários com API REST e cliente desktop.** Projeto modernizado com Python, FastAPI, SQLAlchemy 2.x, Pydantic e SQLite, mantendo o script legado `empresa.py` como referência.

## Arquitetura

- **API REST:** FastAPI com documentação OpenAPI automática.
- **Persistência:** SQLAlchemy 2.x; SQLite por padrão e URL configurável por `DATABASE_URL`.
- **Validação:** Pydantic 2, incluindo salário não negativo e data ISO.
- **Desktop:** cliente Tkinter que consome a API via HTTP.
- **Qualidade:** Pytest e GitHub Actions.

## Requisitos

Python 3.10 ou superior. Para a interface desktop, instale também o suporte Tkinter fornecido pela distribuição Python.

## Instalação

```bash
git clone https://github.com/Foxactive1/Projeto.git
cd Projeto
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

## Executar

Terminal 1 — API local:

```bash
uvicorn employee_manager.api:app --app-dir src --host 127.0.0.1 --port 8000 --reload
```

Documentação interativa: http://127.0.0.1:8000/docs

Terminal 2 — desktop:

```bash
python -m employee_manager.desktop
```

Se necessário, configure `EMPLOYEE_API_URL` para apontar ao endereço da API. A API escuta em `127.0.0.1` por padrão: não a exponha à internet sem autenticação, autorização, TLS e controles de rede.

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | `/health` | Verificação de saúde |
| POST | `/employees` | Cadastrar funcionário |
| GET | `/employees` | Listar funcionários |
| GET | `/employees/{id}` | Consultar funcionário |
| PUT | `/employees/{id}` | Atualizar funcionário |
| DELETE | `/employees/{id}` | Excluir funcionário |

Exemplo de payload:

```json
{
  "nome": "Maria",
  "sobrenome": "Silva",
  "cargo": "Analista de Sistemas",
  "salario": 4500.00,
  "data_contratacao": "2024-01-15"
}
```

## Testes

```bash
pytest -q
```

Os testes usam banco temporário isolado e registros fictícios.

## Banco legado e segurança de dados

O modelo mantém os nomes de tabela e colunas do projeto anterior (`employee`, `nome`, `sobrenome`, `cargo`, `salario`, `data_contratacao`). Isso facilita a transição, mas **não substitui uma validação com uma cópia de backup do banco real**. Faça backup e teste a compatibilidade antes de configurar `DATABASE_URL` para uma base existente. A aplicação não migra automaticamente esquemas antigos.

Arquivos de banco, exportações e segredos locais são ignorados pelo Git. Nunca versione dados pessoais, `.env` ou credenciais.

## Estrutura

```text
src/employee_manager/
  api.py          # API e operações CRUD
  database.py     # Engine e sessões SQLAlchemy
  models.py       # Modelo persistente
  schemas.py      # Contratos Pydantic
  desktop.py      # Cliente Tkinter
 tests/
  test_api.py
```

## Licença

Consulte o arquivo de licença do repositório, se aplicável.

---

Desenvolvido por **Dione Castro Alves | InNovaIdeia®**.
