import sqlite3
import tkinter as tk

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
    status_label.config(text="Tabela criada ou já existente.")

# Função para inserir funcionário
def inserir_funcionario():
    conn = sqlite3.connect('empresa.db')
    cursor = conn.cursor()
    nome = nome_entry.get()
    sobrenome = sobrenome_entry.get()
    cargo = cargo_entry.get()
    salario = float(salario_entry.get())
    data_contratacao = data_contratacao_entry.get()
    cursor.execute("INSERT INTO employee (nome, sobrenome, cargo, salario, data_contratacao) VALUES (?, ?, ?, ?, ?)",
                   (nome, sobrenome, cargo, salario, data_contratacao))
    conn.commit()
    conn.close()
    status_label.config(text="Funcionário inserido com sucesso!")

# Cria da janela principal
root = tk.Tk()
root.title("Gerenciador de Dados dos Funcionarios")

# Criação de rótulos e campos
nome_label = tk.Label(root, text="Nome:")
nome_label.pack()
nome_entry = tk.Entry(root, width=30)
nome_entry.pack()

sobrenome_label = tk.Label(root, text="Sobrenome:")
sobrenome_label.pack()
sobrenome_entry = tk.Entry(root, width=30)
sobrenome_entry.pack()

cargo_label = tk.Label(root, text="Cargo:")
cargo_label.pack()
cargo_entry = tk.Entry(root, width=30)
cargo_entry.pack()

salario_label = tk.Label(root, text="Salário:")
salario_label.pack()
salario_entry = tk.Entry(root, width=30)
salario_entry.pack()

data_contratacao_label = tk.Label(root, text="Data de Contratação (AAAA-MM-DD):")
data_contratacao_label.pack()
data_contratacao_entry = tk.Entry(root, width=30)
data_contratacao_entry.pack()

# Botão para criar a tabela (chamando a função criar_tabela)
criar_tabela_button = tk.Button(root, text="Criar Tabela (ou Verificar Existência)", command=criar_tabela)
criar_tabela_button.pack()

# Botão para inserir funcionário
inserir_funcionario_button = tk.Button(root, text="Inserir Funcionário", command=inserir_funcionario)
inserir_funcionario_button.pack()

# Rótulo de status
status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
