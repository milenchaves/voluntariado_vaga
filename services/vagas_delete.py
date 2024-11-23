import csv
import os
from fastapi import HTTPException

# Configuração do arquivo CSV
CSV_FILE = "csv/vagas.csv"


# Função para deletar uma vaga pelo ID
def deletar_vaga_por_id(id_vaga: int) -> bool:
    if not os.path.exists(CSV_FILE):
        raise HTTPException(status_code=404, detail="Arquivo de vagas não encontrado.")

    vaga_encontrada = False
    linhas_restantes = []

    with open(CSV_FILE, "r") as file:
        reader = csv.reader(file)
        header = next(reader)  # Lê o cabeçalho
        linhas_restantes.append(header)

        for linha in reader:
            if (
                linha and int(linha[0]) == id_vaga
            ):  # Verifica se o ID da linha é igual ao ID fornecido
                vaga_encontrada = True
                continue
            linhas_restantes.append(linha)

    if vaga_encontrada:
        with open(CSV_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(linhas_restantes)
        return True
    else:
        raise HTTPException(
            status_code=404, detail=f"Vaga com ID {id_vaga} não encontrada."
        )
