import csv
import os
import json
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from models import Vaga

# Configuração do arquivo CSV
CSV_FILE = "csv/vagas.csv"

# Inicializando FastAPI
app = FastAPI()


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


# Endpoint para criar uma vaga
@app.post("/vagas/", status_code=201)
def endpoint_criar_vaga(vaga: Vaga):
    return criar_vaga(vaga)


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


# Endpoint para deletar uma vaga
@app.delete("/vagas/{id_vaga}")
def endpoint_deletar_vaga(id_vaga: int):
    if deletar_vaga_por_id(id_vaga):
        return {"msg": f"Vaga com ID {id_vaga} deletada com sucesso."}


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


@app.get("/vagas/")
def endpoint_listar_vagas():
    return listar_todas_vagas()


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


@app.put("/vagas/{id_vaga}")
def endpoint_atualizar_vaga(id_vaga: int, vaga_atualizada: Vaga):
    if atualizar_vaga(id_vaga, vaga_atualizada):
        return {"msg": f"Vaga com ID {id_vaga} atualizada com sucesso."}
