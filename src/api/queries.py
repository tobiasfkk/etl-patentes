# 1. Palavras mais frequentes (total)
TOP_WORDS_ALL = """
SELECT w.word, SUM(f.word_count) AS total
FROM fact_patents f
JOIN dim_words w ON f.word_id = w.id
GROUP BY w.word
ORDER BY total DESC
LIMIT 30;
"""

# 2. Palavras mais frequentes por ano
TOP_WORDS_BY_YEAR = """
SELECT d.year, w.word, SUM(f.word_count) AS total
FROM fact_patents f
JOIN dim_words w ON f.word_id = w.id
JOIN dim_date d ON f.date_id = d.id
GROUP BY d.year, w.word
ORDER BY d.year, total DESC
LIMIT 100;
"""

# 3. Palavras mais frequentes por país
TOP_WORDS_BY_COUNTRY = """
SELECT c.country_name, w.word, SUM(f.word_count) AS total
FROM fact_patents f
JOIN dim_words w ON f.word_id = w.id
JOIN dim_countries c ON f.country_id = c.id
GROUP BY c.country_name, w.word
ORDER BY c.country_name, total DESC
LIMIT 100;
"""

# 4. Palavras mais frequentes por autor
TOP_WORDS_BY_AUTHOR = """
SELECT a.author_name, w.word, SUM(f.word_count) AS total
FROM fact_patents f
JOIN dim_words w ON f.word_id = w.id
JOIN dim_authors a ON f.author_id = a.id
GROUP BY a.author_name, w.word
ORDER BY a.author_name, total DESC
LIMIT 100;
"""

# 5. Palavras associadas à "future" ou "device"
ASSOCIATED_WORDS_SIMPLE = """
WITH patentes_com_redes_generativas AS (
    SELECT DISTINCT f.patent_id
    FROM fact_patents f
    JOIN dim_words w ON f.word_id = w.id
    WHERE w.word = 'future' OR w.word = 'device'
),
palavras_associadas AS (
    SELECT f.word_id, SUM(f.word_count) AS total_count
    FROM fact_patents f
    JOIN patentes_com_redes_generativas p ON f.patent_id = p.patent_id
    GROUP BY f.word_id
),
resultado AS (
    SELECT w.word, pa.total_count
    FROM palavras_associadas pa
    JOIN dim_words w ON pa.word_id = w.id
    WHERE w.word NOT IN ('future', 'device')
)
SELECT *
FROM resultado
ORDER BY total_count DESC
LIMIT 30;
"""

# 6. Palavras associadas por tempo (redes/generativas)
ASSOCIATED_WORDS_OVER_TIME = """
WITH patentes_com_redes_generativas AS (
    SELECT DISTINCT f.patent_id
    FROM fact_patents f
    JOIN dim_words w ON f.word_id = w.id
    WHERE w.word = 'redes' OR w.word = 'generativas'
),
palavras_associadas_com_data AS (
    SELECT f.word_id, f.date_id, SUM(f.word_count) AS total_count
    FROM fact_patents f
    JOIN patentes_com_redes_generativas p ON f.patent_id = p.patent_id
    GROUP BY f.word_id, f.date_id
),
resultado AS (
    SELECT w.word, d.year, d.month, SUM(p.total_count) AS ocorrencias
    FROM palavras_associadas_com_data p
    JOIN dim_words w ON p.word_id = w.id
    JOIN dim_date d ON p.date_id = d.id
    WHERE w.word NOT IN ('redes', 'generativas')
    GROUP BY w.word, d.year, d.month
)
SELECT *
FROM resultado
ORDER BY year, month, ocorrencias DESC
LIMIT 100;
"""

# 7. Ranking das palavras por ano (Top 5)
TOP_WORDS_RANKED_BY_YEAR = """
WITH ranking_palavras AS (
    SELECT d.year, w.word, SUM(f.word_count) AS total,
           ROW_NUMBER() OVER (PARTITION BY d.year ORDER BY SUM(f.word_count) DESC) AS posicao
    FROM fact_patents f
    JOIN dim_words w ON f.word_id = w.id
    JOIN dim_date d ON f.date_id = d.id
    GROUP BY d.year, w.word
)
SELECT *
FROM ranking_palavras
WHERE posicao <= 5
ORDER BY year, posicao;
"""
