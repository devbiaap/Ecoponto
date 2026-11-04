from pydantic import BaseModel, Field


class PontoColetaBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=150)
    descricao: str | None = None
    endereco: str = Field(..., min_length=5, max_length=255)
    bairro: str = Field(..., min_length=2, max_length=100)
    latitude: float | None = None
    longitude: float | None = None
    horario: str | None = Field(None, max_length=150)
    ativo: bool = True


class PontoColetaCreate(PontoColetaBase):
    pass

class PontoColetaUpdate(PontoColetaBase):
    pass

class PontoColetaResponse(PontoColetaBase):
    id: int

    model_config = {
        "from_attributes": True
    }