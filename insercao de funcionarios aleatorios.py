import sqlite3
import random
import names  # Biblioteca para gerar nomes aleatórios

# Função para criar a tabela se não existir
def criar_tabela():
    conn = sqlite3.connect('empresa.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employee (
            id INTEGER PRIMARY KEY,
            nome TEXT,
            sobrenome TEXT,
            cargo TEXT,
            salario REAL,
            data_contratacao DATE
        )
    ''')
    conn.commit()
    conn.close()

# Função para inserir funcionário aleatório
def inserir_funcionario_aleatorio():
    conn = sqlite3.connect('empresa.db')
    cursor = conn.cursor()

    nome = names.get_first_name()
    sobrenome = names.get_last_name()
    cargo = random.choice(['Analista', 'Gerente', 'Desenvolvedor', 'Assistente'])
    salario = round(random.uniform(30000, 80000), 2)
    data_contratacao = f"{random.randint(2000, 2022)}-{random.randint(1, 12)}-{random.randint(1, 28)}"

    cursor.execute("INSERT INTO employee (nome, sobrenome, cargo, salario, data_contratacao) VALUES (?, ?, ?, ?, ?)",
                   (nome, sobrenome, cargo, salario, data_contratacao))
    conn.commit()
    conn.close()

# Criação da tabela
criar_tabela()

# Inserção de 10 funcionários aleatórios
for _ in range(10):
    inserir_funcionario_aleatorio()

print("Inserção de funcionários concluída.")
