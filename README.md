# TCC - Arquitetura de Data Warehouse Automatizado para Apoio à Gestão do Conhecimento em Bases de Patentes

Este projeto realiza a extração, transformação e carga (ETL) de dados de patentes a partir de um arquivo XML para um banco de dados PostgreSQL, utilizando Docker. Além disso, disponibiliza uma API REST para consulta dos dados processados.

Artigo científico: [ARQUITETURA_DE_DATA_WAREHOUSE_AUTOMATIZADO_PARA_APOIO_À_GESTÃO_DO_CONHECIMENTO_EM_BASES_DE_PATENTES.pdf](ARQUITETURA_DE_DATA_WAREHOUSE_AUTOMATIZADO_PARA_APOIO_%C3%80_GEST%C3%83O_DO_CONHECIMENTO_EM_BASES_DE_PATENTES.pdf)

## 📁 Estrutura do Projeto

- **`data/`**: Contém os arquivos XML de entrada e os corrigidos.
    - `dados.xml`: Arquivo XML original com os dados de patentes.
- **`src/etl/`**: Scripts da pipeline ETL:
    - `extract.py`: Extrai dados como título, resumo, descrição, autor, país e data do XML.
    - `transform.py`: Padroniza os dados, extrai palavras únicas e organiza datas.
    - `load.py`: Insere os dados no banco relacional em modelo estrela.
- **`src/database/init_schema.sql`**: Script SQL para criação do esquema do banco de dados.
- **`src/api/`**: Implementação da API REST:
    - `main.py`: Configuração principal da API com FastAPI.
    - `endpoints/`: Endpoints para consulta de patentes, autores e palavras.
    - `queries.py`: Consultas SQL utilizadas pela API.
- **`src/utils/db_connection.py`**: Configuração da conexão com o banco de dados PostgreSQL.
- **`docker-compose.yml`**: Define os serviços Docker (PostgreSQL, ETL e API).
- **`Dockerfile`**: Configura o ambiente Python para o serviço ETL.

## ▶️ Como Executar

### 1. Pré-requisitos

- **Docker** e **Docker Compose** instalados.

### 2. Configurar o Ambiente

1. Baixe o arquivo XML de patentes do site da USPTO ([https://data.uspto.gov/bulkdata/datasets/appxml](https://data.uspto.gov/bulkdata/datasets/appxml)).
2. Coloque o arquivo na pasta `data/` do projeto com o nome `dados.xml`.

### 3. Executar o Projeto

No terminal, execute:

```bash
docker-compose up --build
```

Esse comando irá:

- Subir o PostgreSQL com o schema inicial (`init_schema.sql`);
- Executar o ETL automaticamente após o banco estar disponível;
- Carregar os dados extraídos do XML para o banco.
- Iniciar o serviço da API REST para consulta dos dados.

## Acessar a API

Após a execução, a API estará disponível em [http://localhost:8000](http://localhost:8000). A documentação interativa pode ser acessada em [http://localhost:8000/docs](http://localhost:8000/docs).

### 🧱 Estrutura do Banco de Dados

O banco segue uma modelagem em estrela, com:

#### 🔷 Tabela de Fato

- **`fact_patents`**: Contabiliza a ocorrência de palavras no resumo por patente, data, país e autor.

#### 🔶 Tabelas de Dimensão

- **`dim_authors`**: Informações sobre os autores das patentes.
- **`dim_countries`**: Países associados às patentes.
- **`dim_categories`**: Classificação das patentes (subclasses).
- **`dim_words`**: Palavras únicas extraídas dos resumos.
- **`dim_date`**: Datas associadas às patentes.
- **`dim_patents`**: Informações gerais das patentes (título, número, resumo, descrição).

#### 🛠️ Tabela de Staging

- **`staging_patents`**: Área temporária para armazenar os dados extraídos antes de serem carregados no modelo estrela.

### 🌐 Endpoints da API

A API REST permite consultar os dados processados. Alguns dos principais endpoints:

- **`GET /patents/`**: Lista as patentes cadastradas.
- **`GET /authors/`**: Lista os autores cadastrados.
- **`GET /words/top`**: Retorna as palavras mais frequentes nos resumos.
- **`GET /words/associadas`**: Retorna palavras associadas a termos específicos.

Para mais detalhes, acesse a documentação da API.

### 📊 Consultas SQL Disponíveis

O projeto inclui consultas SQL para análise dos dados, como:

- Palavras mais frequentes por ano, país ou autor;
- Palavras associadas a termos específicos;
- Ranking anual das palavras mais utilizadas.

### 🛠️ Tecnologias Utilizadas

- **Python**: Para a implementação da pipeline ETL e da API.
- **PostgreSQL**: Banco de dados relacional para armazenamento dos dados.
- **Supabase**: Plataforma de banco de dados baseada em PostgreSQL.
- **Docker**: Para containerização dos serviços.
- **FastAPI**: Framework para criação da API REST.