from fastapi import APIRouter
from models import Vaga
from services.vagas_create import criar_vaga
from services.vagas_delete import deletar_vaga_por_id
from services.vagas_get import listar_todas_vagas
from services.vagas_update import atualizar_vaga

router = APIRouter()


# Endpoint para criar uma vaga
@router.post("/vagas/", status_code=201)
def endpoint_criar_vaga(vaga: Vaga):
    return criar_vaga(vaga)


# Endpoint para deletar uma vaga
@router.delete("/vagas/{id_vaga}")
def endpoint_deletar_vaga(id_vaga: int):
    if deletar_vaga_por_id(id_vaga):
        return {"msg": f"Vaga com ID {id_vaga} deletada com sucesso."}


@router.get("/vagas/")
def endpoint_listar_vagas():
    return listar_todas_vagas()


@router.put("/vagas/{id_vaga}")
def endpoint_atualizar_vaga(id_vaga: int, vaga_atualizada: Vaga):
    if atualizar_vaga(id_vaga, vaga_atualizada):
        return {"msg": f"Vaga com ID {id_vaga} atualizada com sucesso."}
