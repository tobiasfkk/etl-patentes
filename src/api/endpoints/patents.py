from fastapi import APIRouter, HTTPException
from src.utils.db_connection import get_db_connection

router = APIRouter()

@router.get("/")
def listar_patentes(limit: int = 10):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, invention_title, doc_number FROM dim_patents LIMIT %s;", (limit,))
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{patent_id}")
def detalhes_patente(patent_id: int):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM dim_patents WHERE id = %s;
        """, (patent_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if not result:
            raise HTTPException(status_code=404, detail="Patente não encontrada")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
