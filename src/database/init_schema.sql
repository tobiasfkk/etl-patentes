-- Tabela de Dimensão: Autores
CREATE TABLE IF NOT EXISTS dim_authors (
    id SERIAL PRIMARY KEY,
    author_name TEXT NOT NULL UNIQUE
);

-- Tabela de Dimensão: Países
CREATE TABLE IF NOT EXISTS dim_countries (
    id SERIAL PRIMARY KEY,
    country_name TEXT NOT NULL UNIQUE
);

-- Tabela de Dimensão: Palavras
CREATE TABLE IF NOT EXISTS dim_words (
    id SERIAL PRIMARY KEY,
    word TEXT NOT NULL UNIQUE
);

-- Tabela de Dimensão: Tempo
CREATE TABLE IF NOT EXISTS dim_date (
    id SERIAL PRIMARY KEY,
    day INTEGER NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL,
    UNIQUE (day, month, year)
);

-- Tabela de Dimensão: Patentes
CREATE TABLE IF NOT EXISTS dim_patents (
    id SERIAL PRIMARY KEY,
    invention_title TEXT NOT NULL UNIQUE,
    doc_number INT NOT NULL UNIQUE,
    abstract_text TEXT NOT NULL,
    description_text TEXT
);

-- Tabela de Fato: Palavras em Patentes
CREATE TABLE IF NOT EXISTS fact_patents (
    patent_id INTEGER NOT NULL,
    word_id INTEGER NOT NULL,
    word_count INTEGER NOT NULL,
    date_id INTEGER NOT NULL,
    country_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    FOREIGN KEY (patent_id) REFERENCES dim_patents (id),
    FOREIGN KEY (word_id) REFERENCES dim_words (id),
    FOREIGN KEY (country_id) REFERENCES dim_countries (id),
    FOREIGN KEY (author_id) REFERENCES dim_authors (id),
    FOREIGN KEY (date_id) REFERENCES dim_date (id)
);

CREATE TABLE IF NOT EXISTS staging_patents (
    id SERIAL PRIMARY KEY,
    doc_number TEXT NOT NULL,
    invention_title TEXT NOT NULL,
    country TEXT NOT NULL,
    application_date DATE,
    author_name TEXT NOT NULL,
    abstract_text TEXT,
    abstract_words TEXT[],  -- Array de palavras
    description_text TEXT,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
