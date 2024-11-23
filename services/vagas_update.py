import csv
import os
from fastapi import HTTPException
from models import Vaga

# Configuração do arquivo CSV
CSV_FILE = "csv/vagas.csv"


# Função para atualizar uma vaga
def atualizar_vaga(id_vaga: int, vaga_atualizada: Vaga) -> bool:
    if not os.path.exists(CSV_FILE):
        raise HTTPException(status_code=404, detail="Arquivo de vagas não encontrado.")

    vaga_encontrada = False
    linhas_atualizadas = []

    with open(CSV_FILE, "r") as file:
        reader = csv.reader(file)
        header = next(reader)
        linhas_atualizadas.append(",".join(header))  # Adiciona o cabeçalho

        for linha in reader:
            if linha:
                if int(linha[0]) == id_vaga:  # Verifica se o ID corresponde
                    vaga_encontrada = True
                    linhas_atualizadas.append(
                        f"{id_vaga},{vaga_atualizada.titulo},{vaga_atualizada.descricao},{vaga_atualizada.organizacao},{vaga_atualizada.data_publicacao},{vaga_atualizada.localizacao}"
                    )
                else:
                    linhas_atualizadas.append(",".join(linha))

    if vaga_encontrada:
        with open(CSV_FILE, "w") as file:
            file.write("\n".join(linhas_atualizadas) + "\n")
        return True
    else:
        raise HTTPException(
            status_code=404, detail=f"Vaga com ID {id_vaga} não encontrada."
        )
