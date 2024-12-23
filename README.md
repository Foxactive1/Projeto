Gerenciador de Dados dos Funcionários

Este projeto é uma aplicação simples em Python que utiliza Tkinter para interface gráfica e SQLite3 para banco de dados. Ele permite criar uma tabela de funcionários, bem como adicionar novos registros de funcionários diretamente pela interface.

Funcionalidades

Criar Tabela: Verifica se a tabela employee existe no banco de dados e a cria caso não exista.

Adicionar Funcionários: Insere novos registros no banco de dados a partir das informações fornecidas pelo usuário na interface gráfica.


Pré-requisitos

Para executar o projeto, é necessário ter instalado:

Python 3.6 ou superior

Bibliotecas padrão:

sqlite3 (inclusa no Python)

tkinter (inclusa no Python)



Como executar

1. Clone o repositório ou baixe o arquivo main.py no seu computador.


2. Execute o arquivo Python no terminal ou em seu IDE preferido:

python main.py


3. Use a interface gráfica para:

Criar a tabela clicando no botão "Criar Tabela (ou Verificar Existência)".

Inserir os dados do funcionário nos campos apropriados e clicar em "Inserir Funcionário".




Estrutura do Banco de Dados

A tabela employee contém os seguintes campos:

Personalização

Para alterar o nome do banco de dados, substitua 'empresa.db' na variável de conexão pelo nome desejado.

Novos campos podem ser adicionados na tabela, mas será necessário atualizar a função inserir_funcionario.


Exemplo de Uso

1. Ao abrir o programa, preencha os seguintes campos:

Nome: Maria

Sobrenome: Silva

Cargo: Analista de Sistemas

Salário: 4500.00

Data de Contratação: 2024-01-15



2. Clique em "Inserir Funcionário".


3. O status na parte inferior da janela exibirá: "Funcionário inserido com sucesso!".



Licença

Este projeto é distribuído sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.


---

Feito com 💻 e ☕ por Dione Castro Alves. vulgo    
InNovaIdeia ®

