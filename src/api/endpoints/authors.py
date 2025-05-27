from fastapi import APIRouter, HTTPException
from src.utils.db_connection import get_db_connection

router = APIRouter()

@router.get("/")
def listar_autores(limit: int = 10):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, author_name FROM dim_authors LIMIT %s;", (limit,))
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{author_name}")
def patentes_por_autor(author_name: str):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT dp.invention_title, dp.doc_number, dd.year
            FROM dim_patents dp
            JOIN fact_patents fp ON dp.id = fp.patent_id
            JOIN dim_authors da ON da.id = fp.author_id
            JOIN dim_date dd ON dd.id = fp.date_id
            WHERE da.author_name ILIKE %s
            GROUP BY dp.invention_title, dp.doc_number, dd.year
            ORDER BY dd.year DESC;
        """, (f"%{author_name}%",))
        result = cur.fetchall()
        cur.close()
        conn.close()
        if not result:
            raise HTTPException(status_code=404, detail="Autor não encontrado ou sem patentes")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
