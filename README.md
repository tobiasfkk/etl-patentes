# Projeto de ETL para Dados de Patentes

Este projeto realiza a extração, transformação e carga (ETL) de dados de patentes a partir de um arquivo XML para um banco de dados PostgreSQL utilizando Docker.

## Estrutura do Projeto

- **`data/dados.xml`**: Arquivo XML com os dados de patentes.
- **`src/etl/`**: Scripts para as etapas de ETL:
  - `extract.py`: Extrai os dados do arquivo XML.
  - `transform.py`: Transforma os dados para o formato do banco de dados.
  - `load.py`: Carrega os dados no banco de dados.
- **`src/database/`**: Scripts SQL para criar as tabelas no banco de dados.
- **`docker-compose.yml`**: Configuração do Docker para PostgreSQL e o serviço Python.
- **`Dockerfile`**: Configuração do ambiente Python.

## Como Executar

1. **Pré-requisitos**:
   - Docker e Docker Compose instalados.

2. **Executar o Projeto**:
   - No terminal, execute:
     ```bash
     docker-compose up --build
     ```
   - Isso irá:
     - Subir o banco de dados PostgreSQL.
     - Executar o script ETL automaticamente.

3. **Verificar os Dados**:
   - Acesse o banco de dados PostgreSQL:
     ```bash
     docker exec -it postgres_patents psql -U postgres -d patents_db
     ```
   - Execute consultas SQL, como:
     ```sql
     SELECT * FROM fact_patents;
     ```

## Estrutura do Banco de Dados

O banco de dados segue uma modelagem multidimensional com:
- **Tabela de Fato**: `fact_patents`
- **Tabelas de Dimensão**:
  - `dim_authors`
  - `dim_countries`
  - `dim_words`
  - `dim_date`
  - `dim_categories`
  - `dim_patents`

## Observações

- Certifique-se de que o arquivo `dados.xml` está no diretório `data`.
- O ETL será executado automaticamente ao iniciar o contêiner Python.

## Contato

Para dúvidas ou sugestões, entre em contato.