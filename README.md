# Projeto de ETL para Dados de Patentes

Este projeto realiza a extração, transformação e carga (ETL) de dados de patentes a partir de um arquivo JSON para um banco de dados PostgreSQL utilizando Docker.

## Estrutura do Projeto

- **`data/dados.json`**: Arquivo JSON com os dados de patentes.
- **`src/etl/`**: Scripts para as etapas de ETL:
  - `extract.py`: Extrai os dados do arquivo JSON.
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
  - `dim_inventors`
  - `dim_applicants`
  - `dim_cpc_classification`
  - `dim_examiners`
  - `dim_addresses`
  - `dim_business_entity_status`
  - `dim_countries`

## Observações

- Certifique-se de que o arquivo [dados.json](http://_vscodecontentref_/1) está no diretório [data](http://_vscodecontentref_/2).
- O ETL será executado automaticamente ao iniciar o contêiner Python.

## Contato

Para dúvidas ou sugestões, entre em contato.