from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from service import (
    listar_datas,
    obter_dados_completos_para_data  # ✅ Importação adicionada
)
from datetime import datetime

app = FastAPI()

# CORS para o frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/api/datas")
def get_datas():
    return listar_datas()

@app.get("/api/analise-completa/{data}")
def get_analise(data: str):
    try:
        return obter_dados_completos_para_data(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
