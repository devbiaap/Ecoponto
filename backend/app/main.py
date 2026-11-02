
from fastapi import FastAPI

app = FastAPI(
    title="EcoPonto API",
    description="API para localização e gerenciamento de pontos de coleta de materiais recicláveis em Sorocaba.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Bem-vindo(a) ao EcoPonto!",
        "description": "Encontre pontos de coleta e descarte seus resíduos corretamente."
    }
