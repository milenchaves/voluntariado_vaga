import csv
import os
import json
from models import Vaga

CSV_FILE = "csv/vagas.csv"


def inicializar_csv():
    if not os.path.exists(CSV_FILE):
        os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)
        with open(CSV_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "id_vaga",
                    "titulo",
                    "descricao",
                    "organizacao",
                    "data_publicacao",
                    "localizacao",
                ]
            )


inicializar_csv()


def obter_proximo_id() -> int:
    if not os.path.exists(CSV_FILE):
        return 1

    with open(CSV_FILE, "r") as file:
        reader = csv.reader(file)
        next(reader)  
        ids = [int(row[0]) for row in reader if row]  
        return max(ids, default=0) + 1 



def criar_vaga(vaga: Vaga):

    vaga.id_vaga = obter_proximo_id()

    vaga_json = vaga.json()

    if not os.path.exists(CSV_FILE):
        inicializar_csv()

    with open(CSV_FILE, "a") as file:
        vaga_dict = json.loads(vaga_json)
        file.write(
            f"{vaga_dict['id_vaga']},{vaga_dict['titulo']},{vaga_dict['descricao']},{vaga_dict['organizacao']},{vaga_dict['data_publicacao']},{vaga_dict['localizacao']}\n"
        )

    return vaga
