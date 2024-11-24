from fastapi import APIRouter
from models import Vaga
from fastapi.responses import JSONResponse
from fastapi import status
import hashlib
import zipfile
import os
from services.vagas_create import criar_vaga
from services.vagas_delete import deletar_vaga_por_id
from services.vagas_get import listar_todas_vagas
from services.vagas_update import atualizar_vaga

router = APIRouter()


CSV_FILE = "csv/vagas.csv"


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
    

# Função hash
@router.get("/vagas/hash")
def endpoint_calcular_hash():

    if not os.path.exists(CSV_FILE):
            raise FileNotFoundError("Arquivo CSV não encontrado.")

    sha256 = hashlib.sha256()

    with open(CSV_FILE, "rb") as file:
        sha256.update(file.read())

    return {"sha256": sha256.hexdigest()}

# Função compactação zip
@router.get("/zip/", status_code=status.HTTP_200_OK)
def endpoint_gerar_zip():

    if not os.path.exists(CSV_FILE):
        raise FileNotFoundError("Arquivo CSV não encontrado.")

    zip_file = CSV_FILE.replace(".csv", ".zip")

    with zipfile.ZipFile(zip_file, "w", compression= zipfile.ZIP_DEFLATED) as file:
            file.write(CSV_FILE, os.path.basename(CSV_FILE))

    return JSONResponse(
        content={"message": "Arquivo CSV compactado com sucesso."}
        )