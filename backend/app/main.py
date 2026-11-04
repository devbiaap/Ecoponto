
from fastapi import FastAPI
from app.routers import ponto_coleta

app = FastAPI(
    title="EcoPonto API",
    description="API para localização e gerenciamento de pontos de coleta de materiais recicláveis em Sorocaba.",
    version="1.0.0"
)

app.include_router(ponto_coleta.router)

@app.get("/")
def home():
    return {
        "message": "Bem-vindo(a) ao EcoPonto!",
        "description": "Encontre pontos de coleta e descarte seus resíduos corretamente."
    }
