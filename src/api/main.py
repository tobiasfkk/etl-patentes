from fastapi import FastAPI
from src.api.endpoints import patents, authors, words

app = FastAPI(title="API de Patentes")

app.include_router(patents.router, prefix="/patents")
app.include_router(authors.router, prefix="/authors")
app.include_router(words.router, prefix="/words")
