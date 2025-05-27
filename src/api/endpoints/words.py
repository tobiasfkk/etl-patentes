from fastapi import APIRouter, HTTPException, Query
from typing import List
from src.utils.db_connection import get_db_connection
from src.api.queries import (
    TOP_WORDS_ALL,
    TOP_WORDS_BY_YEAR,
    TOP_WORDS_BY_COUNTRY,
    TOP_WORDS_BY_AUTHOR,
    ASSOCIATED_WORDS_SIMPLE,
    ASSOCIATED_WORDS_OVER_TIME,
    TOP_WORDS_RANKED_BY_YEAR
)

router = APIRouter()

def run_query(sql: str):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/top")
def palavras_mais_frequentes():
    return run_query(TOP_WORDS_ALL)


@router.get("/por-ano")
def palavras_por_ano():
    return run_query(TOP_WORDS_BY_YEAR)


@router.get("/por-pais")
def palavras_por_pais():
    return run_query(TOP_WORDS_BY_COUNTRY)


@router.get("/por-autor")
def palavras_por_autor():
    return run_query(TOP_WORDS_BY_AUTHOR)


@router.get("/associadas")
def associadas_a_termos(termos: List[str] = Query(..., description="Lista de palavras alvo, separadas por vírgula")):
    if not termos or len(termos) < 1:
        raise HTTPException(status_code=400, detail="Você deve informar pelo menos uma palavra.")

    termos_sql = ", ".join([f"'{t.strip()}'" for t in termos])

    sql = f"""
    WITH patentes_com_termos AS (
        SELECT DISTINCT f.patent_id
        FROM fact_patents f
        JOIN dim_words w ON f.word_id = w.id
        WHERE w.word IN ({termos_sql})
    ),
    palavras_associadas AS (
        SELECT f.word_id, SUM(f.word_count) AS total_count
        FROM fact_patents f
        JOIN patentes_com_termos p ON f.patent_id = p.patent_id
        GROUP BY f.word_id
    ),
    resultado AS (
        SELECT w.word, pa.total_count
        FROM palavras_associadas pa
        JOIN dim_words w ON pa.word_id = w.id
        WHERE w.word NOT IN ({termos_sql})
    )
    SELECT *
    FROM resultado
    ORDER BY total_count DESC
    LIMIT 30;
    """

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/associadas-tempo")
def associadas_com_tempo(termos: List[str] = Query(..., description="Lista de palavras alvo, separadas por vírgula")):
    if not termos or len(termos) < 1:
        raise HTTPException(status_code=400, detail="Você deve informar pelo menos uma palavra.")

    termos_sql = ", ".join([f"'{t.strip()}'" for t in termos])

    sql = f"""
    WITH patentes_com_termos AS (
        SELECT DISTINCT f.patent_id
        FROM fact_patents f
        JOIN dim_words w ON f.word_id = w.id
        WHERE w.word IN ({termos_sql})
    ),
    palavras_associadas_com_data AS (
        SELECT f.word_id, f.date_id, SUM(f.word_count) AS total_count
        FROM fact_patents f
        JOIN patentes_com_termos p ON f.patent_id = p.patent_id
        GROUP BY f.word_id, f.date_id
    ),
    resultado AS (
        SELECT w.word, d.year, d.month, SUM(p.total_count) AS ocorrencias
        FROM palavras_associadas_com_data p
        JOIN dim_words w ON p.word_id = w.id
        JOIN dim_date d ON p.date_id = d.id
        WHERE w.word NOT IN ({termos_sql})
        GROUP BY w.word, d.year, d.month
    )
    SELECT *
    FROM resultado
    ORDER BY year, month, ocorrencias DESC
    LIMIT 100;
    """

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ranking-anual")
def ranking_anual_top5():
    return run_query(TOP_WORDS_RANKED_BY_YEAR)
