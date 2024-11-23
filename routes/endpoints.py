import csv
import os
import json
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from models import Vaga

# Endpoint para criar uma vaga
@app.post("/vagas/", status_code=201)
def endpoint_criar_vaga(vaga: Vaga):
    return criar_vaga(vaga)


# Endpoint para deletar uma vaga
@app.delete("/vagas/{id_vaga}")
def endpoint_deletar_vaga(id_vaga: int):
    if deletar_vaga_por_id(id_vaga):
        return {"msg": f"Vaga com ID {id_vaga} deletada com sucesso."}
    

@app.get("/vagas/")
def endpoint_listar_vagas():
    return listar_todas_vagas()

@app.put("/vagas/{id_vaga}")
def endpoint_atualizar_vaga(id_vaga: int, vaga_atualizada: Vaga):
    if atualizar_vaga(id_vaga, vaga_atualizada):
        return {"msg": f"Vaga com ID {id_vaga} atualizada com sucesso."}