import csv
import os
from models import Vaga

# Configuração do arquivo CSV
CSV_FILE = "csv/vagas.csv"


# Função para listar todas as vagas
def listar_todas_vagas():
    if not os.path.exists(CSV_FILE):
        print("Nenhuma vaga encontrada. O arquivo ainda não foi criado.")
        return []

    vagas = []

    with open(CSV_FILE, "r") as file:
        reader = csv.reader(file)
        header = next(reader, None)  # Pular o cabeçalho
        if header is None:
            print("O arquivo está vazio ou sem cabeçalho.")
            return []

        for linha in reader:
            if linha:
                vagas.append(
                    Vaga(
                        id_vaga=int(linha[0]),
                        titulo=linha[1],
                        descricao=linha[2],
                        organizacao=linha[3],
                        data_publicacao=linha[4],
                        localizacao=linha[5],
                    )
                )

    return vagas
