from pydantic import BaseModel
from datetime import date


class Vaga(BaseModel):
    id_vaga: int
    titulo: str
    descricao: str
    organizacao: str
    data_publicacao: date
    localizacao: str
