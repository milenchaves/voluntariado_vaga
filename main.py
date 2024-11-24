from fastapi import FastAPI
from routes.endpoints import router as rota_vagas

# Configuração do arquivo CSV
CSV_FILE = "csv/vagas.csv"

# Inicializando FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"msg": "Vagas para voluntariado"}

app.include_router(rota_vagas, prefix="/api", tags=["Vagas"])
