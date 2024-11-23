import csv
import os
import json
from models import Vaga

CSV_FILE = "csv/vagas.csv"


# Função para inicializar o arquivo CSV
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


# Função para obter o próximo ID disponível
def obter_proximo_id() -> int:
    if not os.path.exists(CSV_FILE):
        return 1

    with open(CSV_FILE, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Pular o cabeçalho
        ids = [int(row[0]) for row in reader if row]  # Coleta os IDs existentes
        return max(ids, default=0) + 1  # Retorna o maior ID + 1 ou 1 se estiver vazio


# Função para criar uma nova vaga
def criar_vaga(vaga: Vaga):
    # Gerar automaticamente o próximo ID
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
