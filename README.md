# Projeto de ETL para Dados de Patentes

Este projeto realiza a extração, transformação e carga (ETL) de dados de patentes a partir de um arquivo XML para um banco de dados PostgreSQL utilizando Docker.

## 📁 Estrutura do Projeto

- `data/dados.xml`: Arquivo XML com os dados de patentes.
- `src/etl/`: Scripts da pipeline ETL:
    - `extract.py`: Extrai dados como título, resumo, descrição, autor, país e data.
    - `transform.py`: Padroniza os dados, extrai palavras únicas e organiza datas.
    - `load.py`: Insere os dados no banco relacional em modelo estrela.
- `src/database/init_schema.sql`: Script SQL de criação do esquema de banco.
- `src/utils/db_connection.py`: Conexão ao PostgreSQL via psycopg2.
- `docker-compose.yml`: Define os serviços (PostgreSQL + contêiner ETL).
- `Dockerfile`: Configura o ambiente Python para o serviço ETL.

## ▶️ Como Executar

### 1. Pré-requisitos

- Docker e Docker Compose instalados.

### 2. Baixar arquivo XML de Patentes da USPTO

Baixe o arquivo XML de patentes do site da USPTO ([https://data.uspto.gov/bulkdata/datasets/appxml](https://data.uspto.gov/bulkdata/datasets/appxml)) e coloque-o na pasta `data/` do projeto. O arquivo deve ser nomeado `dados.xml`.
### 2. Rodar o pipeline ETL

No terminal, execute:

    docker-compose up --build

Esse comando irá:

- Subir o PostgreSQL com o schema inicial (`init_schema.sql`);
- Executar o ETL automaticamente após o banco estar disponível;
- Carregar os dados extraídos do XML para o banco.

## 🧱 Estrutura do Banco de Dados

O banco segue uma modelagem em estrela, com:

### 🔷 Tabela de Fato

- `fact_patents`: Contabiliza a ocorrência de palavras no resumo por patente, data, país e autor.

### 🔶 Tabelas de Dimensão

- `dim_authors`: Nome dos autores (inventores).
- `dim_countries`: País da publicação.
- `dim_words`: Palavras únicas extraídas do resumo (`abstract`).
- `dim_date`: Dia, mês e ano da publicação.
- `dim_patents`: Título da invenção, resumo e descrição completa.

## 📝 Observações

- O ETL extrai e armazena:
    - Título, país, número do documento, tipo, data de publicação;
    - Nome do inventor;
    - Texto do resumo (**abstract**) e **descrição completa**.
- O script transforma o resumo em palavras únicas, contabiliza suas ocorrências e as armazena na tabela fato.
- As Stopwords são removidas do resumo para evitar poluição dos dados.
- O arquivo `dados.xml` deve estar presente na pasta `data/` antes de rodar o ETL.

## ❓ Contato

Em caso de dúvidas ou sugestões, sinta-se à vontade para abrir uma *issue* ou entrar em contato.
