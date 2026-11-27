# Employee Manager — API + Desktop

Aplicação de gerenciamento de funcionários modernizada com **FastAPI**, **SQLAlchemy**, **SQLite** e interface desktop **CustomTkinter**. A interface desktop consome a API REST, mantendo a camada de dados independente da interface.

> **Privacidade:** bancos de dados, exportações e registros reais não fazem parte desta versão do projeto. Use somente dados fictícios em desenvolvimento e testes. O arquivo `.env.example` contém apenas configurações ilustrativas.

## Arquitetura

- **API:** FastAPI com documentação OpenAPI automática.
- **Persistência:** SQLAlchemy 2.x e SQLite por padrão.
- **Desktop:** CustomTkinter + Requests.
- **Validação:** Pydantic, incluindo salário não negativo e data ISO.
- **Testes:** Pytest + FastAPI TestClient.

## Estrutura

```text
src/employee_manager/
  api.py          # endpoints REST e factory da aplicação
  database.py     # engine e sessões SQLAlchemy
  models.py       # mapeamento da tabela employee
  schemas.py      # contratos e validação Pydantic
  desktop.py      # interface desktop
tests/
  test_api.py
requirements.txt
.env.example
```

## Instalação

Recomendado: Python 3.10 ou superior. Para a interface gráfica, instale também os componentes Tcl/Tk exigidos pelo sistema operacional.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Executar

Terminal 1 — API:

```bash
# Linux/macOS
PYTHONPATH=src uvicorn employee_manager.api:app --reload
# Windows PowerShell
$env:PYTHONPATH="src"; uvicorn employee_manager.api:app --reload
```

Documentação interativa: http://127.0.0.1:8000/docs

Terminal 2 — Desktop:

```bash
# Linux/macOS
PYTHONPATH=src python -m employee_manager.desktop
# Windows PowerShell
$env:PYTHONPATH="src"; python -m employee_manager.desktop
```

A API cria a tabela `employee` ao iniciar. Por padrão, o banco local é `empresa.db`. Para usar outro caminho, configure `DATABASE_URL`; para apontar o desktop a outra API, configure `API_BASE_URL`.

## Endpoints

| Método | Rota | Ação |
|---|---|---|
| GET | `/health` | Verifica a API |
| GET | `/employees` | Lista funcionários |
| POST | `/employees` | Cadastra funcionário |
| GET | `/employees/{id}` | Consulta funcionário |
| PUT | `/employees/{id}` | Atualiza funcionário |
| DELETE | `/employees/{id}` | Exclui funcionário |

## Testes

```bash
PYTHONPATH=src pytest -q
```

Os testes usam banco SQLite em memória e dados inteiramente fictícios.

## Compatibilidade e migração

O modelo mantém os nomes de tabela e colunas da aplicação original (`employee`, `id`, `nome`, `sobrenome`, `cargo`, `salario`, `data_contratacao`). Faça backup local e valide o formato do banco antes de apontar `DATABASE_URL` para uma base existente. Não coloque arquivos de banco ou exportações no Git.

## Segurança operacional

- Não versionar bancos, dumps, planilhas ou dados pessoais.
- Não publicar credenciais ou arquivos `.env`.
- Restringir a API à rede confiável enquanto não houver autenticação e autorização.
- Antes de uso em produção, adicionar autenticação, autorização por perfil, auditoria, política de retenção e backup criptografado.

## Licença

Consulte o arquivo de licença do repositório, se aplicável.
