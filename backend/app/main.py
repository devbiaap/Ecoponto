from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import ponto_coleta, material, ponto_material


app = FastAPI(
    title="EcoPonto API",
    description="API para localização e gerenciamento de pontos de coleta de materiais recicláveis em Sorocaba.",
    version="1.0.0"
)


# Configuração do CORS
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(ponto_coleta.router)
app.include_router(material.router)
app.include_router(ponto_material.router)


@app.get("/")
def home():
    return {
        "message": "Bem-vindo(a) ao EcoPonto!",
        "description": "Encontre pontos de coleta e descarte seus resíduos corretamente."
    }
